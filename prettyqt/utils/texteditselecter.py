from __future__ import annotations

import contextlib
from collections.abc import Iterator
import logging
import re
from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui
from prettyqt.utils import colors, datatypes

logger = logging.getLogger(__name__)

SEARCH_REGEX = re.compile(r"([^/]|\\/)+$")
SEARCH_FLAGS_REGEX = re.compile(r"([^/]|\\/)*?([^\\]/[biw]*)$")
REPLACE_REGEX = re.compile(
    r"""
    (?P<search>([^/]|\\/)*?[^\\])/(?P<replace>(([^/]|\\/)*[^\\])?)/(?P<flags>[abiw]*)$
""",
    re.VERBOSE,
)


class TextEditSelecter:
    def __init__(self, widget):
        self._widget = widget
        self._current_block = None
        self.search_buffer: str | None = None
        self.search_flags = None

    def __getitem__(self, index: int | slice):
        doc = self._widget.document()
        if isinstance(index, int):
            return doc.findBlockByNumber(index)
        start = doc.findBlockByNumber(index.start)
        end = doc.findBlockByNumber(index.stop)
        blocks = [start]
        while start != end and start.isValid():
            start = start.next()
            blocks.append(start)
        return blocks

    def goto_line(self, line_no: int, end_pos: Literal["top", "bottom"] | None = None):
        doc = self._widget.document()
        match end_pos:
            case "top":
                self._widget.moveCursor(gui.TextCursor.MoveOperation.End)
            case "bottom":
                self._widget.moveCursor(gui.TextCursor.MoveOperation.Start)
        lines = doc.blockCount()
        assert 1 <= line_no <= lines
        pos = doc.findBlockByLineNumber(line_no - 1).position()
        with self.current_cursor() as text_cursor:
            text_cursor.setPosition(pos)

    def get_selected_text(self) -> str:
        if self._widget.textCursor().hasSelection():
            return self._widget.textCursor().selectedText()
        else:
            return ""

    def highlight_current_line(self, color: datatypes.ColorType = None):
        if color is None:
            color = self._widget.get_palette().get_color("highlight")
        else:
            color = colors.get_color(color)
        extra_selections = []

        if not self._widget.isReadOnly():
            selection = widgets.TextEdit.ExtraSelection()
            selection.format.setBackground(color)
            prop = QtGui.QTextFormat.Property.FullWidthSelection
            selection.format.setProperty(prop, True)
            selection.cursor = self._widget.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self._widget.setExtraSelections(extra_selections)

    def select_text(self, start: int, end: int):
        with self.create_cursor() as c:
            c.select_text(start, end)

    def _update_on_block_change(self):
        tc = self._widget.textCursor()
        b = tc.blockNumber()
        if b == self._current_block:
            return
        self._current_block = b
        self._widget.viewport().update()

    def get_current_line(self) -> int:
        return self._widget.textCursor().blockNumber()

    def get_selected_block_span(self) -> tuple[int, int]:
        start = self._widget.textCursor().selectionStart()
        end = self._widget.textCursor().selectionEnd()
        start_block_id = self._widget.document().findBlock(start).blockNumber()
        end_block_id = self._widget.document().findBlock(end).blockNumber()

        return (start_block_id, end_block_id)

    @contextlib.contextmanager
    def create_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self._widget.document())
        yield cursor
        self._widget.setTextCursor(cursor)

    @contextlib.contextmanager
    def current_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self._widget.textCursor())
        yield cursor
        self._widget.setTextCursor(cursor)

    def get_text_cursor(self) -> gui.TextCursor:
        return gui.TextCursor(self._widget.textCursor())

    def move_cursor(
        self,
        operation: gui.textcursor.MoveOperationStr,
        mode: gui.textcursor.MoveModeStr = "move",
    ):
        self._widget.moveCursor(
            gui.textcursor.MOVE_OPERATION[operation], gui.textcursor.MOVE_MODE[mode]
        )

    def search_and_replace(self, arg: str):
        """Main search and replace function.

        arg is a string with a vim-like s&r syntax (see the regexes below)
        """

        def generate_flags(flagstr: str):
            self.search_flags = QtGui.QTextDocument.FindFlag(0)
            if "b" in flagstr:
                self.search_flags |= QtGui.QTextDocument.FindFlag.FindBackward
            if "i" not in flagstr:
                self.search_flags |= QtGui.QTextDocument.FindFlag.FindCaseSensitively
            if "w" in flagstr:
                self.search_flags |= QtGui.QTextDocument.FindFlag.FindWholeWords

        if search_match := SEARCH_REGEX.match(arg):
            self.search_buffer = search_match[0]
            self.search_flags = QtGui.QTextDocument.FindFlag.FindCaseSensitively
            self.search_next()
        elif search_flags_match := SEARCH_FLAGS_REGEX.match(arg):
            self.search_buffer, flags = search_flags_match[0].rsplit("/", 1)
            generate_flags(flags)
            self.search_next()
        elif replace_match := REPLACE_REGEX.match(arg):
            self.search_buffer = replace_match.group("search")
            generate_flags(replace_match.group("flags"))
            if "a" in replace_match.group("flags"):
                self._replace_all(replace_match.group("replace"))
            else:
                self._replace_next(replace_match.group("replace"))
        else:
            logger.error("Malformed search/replace expression")

    def _searching_backwards(self) -> bool:
        return bool(QtGui.QTextDocument.FindFlag.FindBackward & self.search_flags)

    def search_next(self):
        """Go to the next string found.

        This does the same thing as running the same search-command again.
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self._widget.textCursor()
        if not self._widget.find(self.search_buffer, self.search_flags):
            if not self._widget.textCursor().atStart() or (
                self._searching_backwards() and not self._widget.textCursor().atEnd()
            ):
                self.move_cursor("end" if self._searching_backwards() else "start")
                if not self._widget.find(self.search_buffer, self.search_flags):
                    self._widget.setTextCursor(temp_cursor)
                    logger.error("Text not found")
            else:
                self._widget.setTextCursor(temp_cursor)
                logger.error("Text not found")

    def _replace_next(self, replace_buffer: str) -> None:
        """Go to the next string found and replace it with replace_buffer.

        While this technically can be called from outside this class, it is
        not recommended (and most likely needs some modifications of the code.)
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self._widget.textCursor()
        found = self._widget.find(self.search_buffer, self.search_flags)
        if not found and (
            not self._widget.textCursor().atStart()
            or (self._searching_backwards() and not self._widget.textCursor().atEnd())
        ):
            self.move_cursor("end" if self._searching_backwards() else "start")
            found = self._widget.find(self.search_buffer, self.search_flags)
            if not found:
                self._widget.setTextCursor(temp_cursor)
        if found:
            t = self._widget.textCursor()
            t.insertText(replace_buffer)
            length = len(replace_buffer)
            t.setPosition(t.position() - length)
            t.setPosition(t.position() + length, QtGui.QTextCursor.MoveMode.KeepAnchor)
            self._widget.setTextCursor(t)
            logger.info(f"Replaced on line {t.blockNumber()}, pos {t.positionInBlock()}")
        else:
            logger.error("Text not found")

    def _replace_all(self, replace_buffer: str) -> None:
        """Replace all strings found with the replace_buffer.

        As with replace_next, you probably don't want to call this manually.
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self._widget.textCursor()
        times = 0
        self.move_cursor("start")
        while self._widget.find(self.search_buffer, self.search_flags):
            self._widget.textCursor().insertText(replace_buffer)
            times += 1
        if times:
            logger.info(f'{times} instance{"s" if times else ""} replaced')
        else:
            logger.error("Text not found")
        self._widget.setTextCursor(temp_cursor)

    def highlight_matches(
        self, pattern: str, highlight_color: datatypes.ColorType = "red"
    ):
        color = colors.get_color(highlight_color)
        cursor = self._widget.get_text_cursor()
        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(QtGui.QBrush(color))
        re = core.RegularExpression(pattern)
        for match in re.global_match(self._widget.toPlainText()):
            cursor.set_position(match.capturedStart(), "move")
            cursor.set_position(match.capturedEnd(), "keep")
            cursor.mergeCharFormat(fmt)

    def replace_block_at_cursor(self, new_text: str):
        cursor = self._widget.textCursor()
        cursor.select(QtGui.QTextCursor.MoveOperation.BlockUnderCursor)
        if cursor.selectionStart() != 0:
            new_text = "\n" + new_text
        cursor.removeSelectedText()
        cursor.insertText(new_text)


if __name__ == "__main__":
    app = widgets.app()

    test = widgets.PlainTextEdit()
    for i in range(200):
        test.append_text(str(i))
    test.show()
    with app.debug_mode():
        app.sleep(2)
        print(test.selecter[20:50])
        app.exec()
