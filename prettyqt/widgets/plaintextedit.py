from __future__ import annotations

from collections.abc import Iterator
import contextlib
from typing import Literal

from deprecated import deprecated

from prettyqt import constants, core, gui, syntaxhighlighters, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, colors, types


LINE_WRAP_MODE = bidict(
    none=QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap,
    widget_width=QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth,
)

LineWrapModeStr = Literal["none", "widget_width"]


QtWidgets.QPlainTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class PlainTextEdit(QtWidgets.QPlainTextEdit):

    value_changed = core.Signal()

    def __init__(
        self,
        text: str = "",
        parent: QtWidgets.QWidget | None = None,
        read_only: bool = False,
    ):
        super().__init__(parent)
        self._allow_wheel_zoom = False
        self.validator: QtGui.QValidator | None = None
        self.textChanged.connect(self._on_value_change)
        self.set_read_only(read_only)
        doc = gui.TextDocument(self)
        layout = widgets.PlainTextDocumentLayout(doc)
        doc.setDocumentLayout(layout)
        self.setDocument(doc)
        self.set_text(text)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            read_only=self.isReadOnly(),
            line_wrap_mode=self.get_line_wrap_mode(),
            word_wrap_mode=self.get_word_wrap_mode(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_text(state["text"])
        self.setReadOnly(state["read_only"])
        self.set_line_wrap_mode(state["line_wrap_mode"])
        self.set_word_wrap_mode(state["word_wrap_mode"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str):
        self.append_text(other)
        return self

    def wheelEvent(self, event):
        """Handle wheel event for zooming."""
        if not self._allow_wheel_zoom:
            return None
        if event.modifiers() & constants.CTRL_MOD:
            self.zoomIn() if event.angleDelta().y() > 0 else self.zoomOut()
        else:
            super().wheelEvent(event)

    def allow_wheel_zoom(self, do_zoom: bool = True):
        self._allow_wheel_zoom = do_zoom

    def goto_line(self, line_no: int):
        doc = self.document()
        lines = doc.blockCount()
        assert 1 <= line_no <= lines
        pos = doc.findBlockByLineNumber(line_no - 1).position()
        with self.current_cursor() as text_cursor:
            text_cursor.setPosition(pos)

    def get_selected_text(self) -> str:
        if self.textCursor().hasSelection():
            return self.textCursor().selectedText()
        else:
            return ""

    def get_current_line(self) -> int:
        return self.textCursor().blockNumber()

    def get_selected_rows(self) -> tuple[int, int]:
        start = self.textCursor().selectionStart()
        end = self.textCursor().selectionEnd()
        start_block_id = self.document().findBlock(start).blockNumber()
        end_block_id = self.document().findBlock(end).blockNumber()

        return (start_block_id, end_block_id)

    @contextlib.contextmanager
    def create_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self.document())
        yield cursor
        self.setTextCursor(cursor)

    @contextlib.contextmanager
    def current_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self.textCursor())
        yield cursor
        self.setTextCursor(cursor)

    def get_text_cursor(self) -> gui.TextCursor:
        return gui.TextCursor(self.textCursor())

    def move_cursor(
        self,
        operation: gui.textcursor.MoveOperationStr,
        mode: gui.textcursor.MoveModeStr = "move",
    ):
        self.moveCursor(
            gui.textcursor.MOVE_OPERATION[operation], gui.textcursor.MOVE_MODE[mode]
        )

    def append_text(self, text: str, newline: bool = True):
        if newline:
            self.appendPlainText(text)
        else:
            self.move_cursor("end")
            self.insertPlainText(text)
            self.move_cursor("end")

    def set_text(self, text: str):
        self.setPlainText(text)

    def set_syntaxhighlighter(self, syntax: str, style: str | None = None):
        self._hl = syntaxhighlighters.PygmentsHighlighter(self.document(), syntax)
        if style is not None:
            self._hl.set_style(style)

    def text(self) -> str:
        return self.toPlainText()

    def select_text(self, start: int, end: int):
        with self.create_cursor() as c:
            c.select_text(start, end)

    def set_read_only(self, value: bool = True):
        """Make the PlainTextEdit read-only.

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def show_whitespace_and_tabs(self, show: bool):
        """Set show white spaces flag."""
        doc = self.document()
        options = doc.defaultTextOption()
        flag = QtGui.QTextOption.Flag.ShowTabsAndSpaces
        if show:
            options.setFlags(options.flags() | flag)  # type: ignore
        else:
            options.setFlags(options.flags() & ~flag)  # type: ignore
        doc.setDefaultTextOption(options)

    def highlight_current_line(self, color: types.ColorType = None):
        if color is None:
            color = self.get_palette().get_color("highlight")
        else:
            color = colors.get_color(color)
        extra_selections = []

        if not self.isReadOnly():
            selection = widgets.TextEdit.ExtraSelection()
            selection.format.setBackground(color)
            prop = QtGui.QTextFormat.Property.FullWidthSelection
            selection.format.setProperty(prop, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    @deprecated(reason="This method is deprecated, use set_word_wrap_mode instead.")
    def set_wrap_mode(self, mode: gui.textoption.WordWrapModeStr):
        self.set_word_wrap_mode(mode)

    def set_word_wrap_mode(self, mode: gui.textoption.WordWrapModeStr):
        """Set word wrap mode.

        Args:
            mode: word wrap mode to use

        Raises:
            InvalidParamError: wrap mode does not exist
        """
        if mode not in gui.textoption.WORD_WRAP_MODE:
            raise InvalidParamError(mode, gui.textoption.WORD_WRAP_MODE)
        self.setWordWrapMode(gui.textoption.WORD_WRAP_MODE[mode])

    @deprecated(reason="This method is deprecated, use get_word_wrap_mode instead.")
    def get_wrap_mode(self) -> gui.textoption.WordWrapModeStr:
        return self.get_word_wrap_mode()

    def get_word_wrap_mode(self) -> gui.textoption.WordWrapModeStr:
        """Get the current word wrap mode.

        Returns:
            Word wrap mode
        """
        return gui.textoption.WORD_WRAP_MODE.inverse[self.wordWrapMode()]

    def set_line_wrap_mode(self, mode: LineWrapModeStr):
        """Set line wrap mode.

        Args:
            mode: line wrap mode to use

        Raises:
            InvalidParamError: line wrap mode does not exist
        """
        if mode not in LINE_WRAP_MODE:
            raise InvalidParamError(mode, LINE_WRAP_MODE)
        self.setLineWrapMode(LINE_WRAP_MODE[mode])

    def get_line_wrap_mode(self) -> LineWrapModeStr:
        """Get the current wrap mode.

        Returns:
            Wrap mode
        """
        return LINE_WRAP_MODE.inverse[self.lineWrapMode()]

    def _on_value_change(self):
        self.value_changed.emit()
        if self.validator is not None:
            self._set_validation_color()

    def _set_validation_color(self, state: bool = True):
        color = "orange" if not self.is_valid() else None
        self.set_background_color(color)

    def set_validator(self, validator: QtGui.QValidator | None):
        self.validator = validator
        self._set_validation_color()

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegularExpressionValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def is_valid(self) -> bool:
        if self.validator is None:
            return True
        return self.validator.is_valid_value(self.text())

    def set_value(self, value: str):
        self.setPlainText(value)

    def get_value(self) -> str:
        return self.text()


if __name__ == "__main__":
    from prettyqt import custom_validators

    val = custom_validators.RegexPatternValidator()
    app = widgets.app()
    widget = PlainTextEdit("This is a test")
    widget.show_whitespace_and_tabs(True)
    widget.set_validator(val)
    with widget.current_cursor() as c:
        c.select_text(2, 4)
    widget.show()
    app.main_loop()
