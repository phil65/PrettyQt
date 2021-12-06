from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


MOVE_MODE = bidict(
    move=QtGui.QTextCursor.MoveMode.MoveAnchor, keep=QtGui.QTextCursor.MoveMode.KeepAnchor
)

MoveModeStr = Literal["move", "keep"]

MOVE_OPERATION = bidict(
    no_move=QtGui.QTextCursor.MoveOperation.NoMove,
    start=QtGui.QTextCursor.MoveOperation.Start,
    start_of_line=QtGui.QTextCursor.MoveOperation.StartOfLine,
    start_of_block=QtGui.QTextCursor.MoveOperation.StartOfBlock,
    start_of_word=QtGui.QTextCursor.MoveOperation.StartOfWord,
    previous_block=QtGui.QTextCursor.MoveOperation.PreviousBlock,
    previous_char=QtGui.QTextCursor.MoveOperation.PreviousCharacter,
    previous_word=QtGui.QTextCursor.MoveOperation.PreviousWord,
    up=QtGui.QTextCursor.MoveOperation.Up,
    left=QtGui.QTextCursor.MoveOperation.Left,
    word_left=QtGui.QTextCursor.MoveOperation.WordLeft,
    end=QtGui.QTextCursor.MoveOperation.End,
    end_of_line=QtGui.QTextCursor.MoveOperation.EndOfLine,
    end_of_word=QtGui.QTextCursor.MoveOperation.EndOfWord,
    end_of_block=QtGui.QTextCursor.MoveOperation.EndOfBlock,
    next_block=QtGui.QTextCursor.MoveOperation.NextBlock,
    next_char=QtGui.QTextCursor.MoveOperation.NextCharacter,
    next_word=QtGui.QTextCursor.MoveOperation.NextWord,
    down=QtGui.QTextCursor.MoveOperation.Down,
    right=QtGui.QTextCursor.MoveOperation.Right,
    word_right=QtGui.QTextCursor.MoveOperation.WordRight,
    next_cell=QtGui.QTextCursor.MoveOperation.NextCell,
    previous_cell=QtGui.QTextCursor.MoveOperation.PreviousCell,
    next_row=QtGui.QTextCursor.MoveOperation.NextRow,
    previous_row=QtGui.QTextCursor.MoveOperation.PreviousRow,
)

MoveOperationStr = Literal[
    "no_move",
    "start",
    "start_of_line",
    "start_of_block",
    "start_of_word",
    "previous_block",
    "previous_char",
    "previous_word",
    "up",
    "left",
    "word_left",
    "end",
    "end_of_line",
    "end_of_word",
    "end_of_block",
    "next_block",
    "next_char",
    "next_word",
    "down",
    "right",
    "word_right",
    "next_cell",
    "previous_cell",
    "next_row",
    "previous_row",
]

SELECTION_TYPE = bidict(
    document=QtGui.QTextCursor.SelectionType.Document,
    block_under_cursor=QtGui.QTextCursor.SelectionType.BlockUnderCursor,
    line_under_cursor=QtGui.QTextCursor.SelectionType.LineUnderCursor,
    word_under_cursor=QtGui.QTextCursor.SelectionType.WordUnderCursor,
)

SelectionTypeStr = Literal[
    "document", "block_under_cursor", "line_under_cursor", "word_under_cursor"
]


class TextCursor(QtGui.QTextCursor):
    def __str__(self):
        return self.selectedText().replace("\u2029", "\n")

    def move_position(
        self, operation: MoveOperationStr, mode: MoveModeStr = "move", n: int = 1
    ) -> bool:
        return self.movePosition(MOVE_OPERATION[operation], MOVE_MODE[mode], n)

    def set_position(self, pos: int, mode: MoveModeStr = "move"):
        """Set cursor to given position.

        Args:
            pos: Cursor position
            mode: Move mode
        """
        self.setPosition(pos, MOVE_MODE[mode])

    def select(self, selection: SelectionTypeStr | QtGui.QTextCursor.SelectionType):
        if isinstance(selection, QtGui.QTextCursor.SelectionType):
            sel = selection
        else:
            sel = SELECTION_TYPE[selection]
        super().select(sel)

    def span(self) -> tuple[int, int]:
        return (self.anchor(), self.position())

    def get_cursor_position(self) -> tuple[int, int]:
        """Return the QTextCursor position.

        The position is a tuple made up of
        the line number (0 based) and the column number (0 based).
        :return: tuple(line, column)
        """
        return (self.blockNumber(), self.columnNumber())

    def get_selection(self) -> gui.TextDocumentFragment:
        return gui.TextDocumentFragment(self.selection())

    def select_text(
        self,
        start_pos: int | MoveOperationStr,
        end_pos: int | MoveOperationStr,
    ) -> str:
        """Select text from start position to end position.

        Positions can be either an integer index or a move operation

        Args:
            start_pos: Start position
            end_pos: End position
        """
        if isinstance(start_pos, int):
            self.set_position(start_pos)
        else:
            self.move_position(start_pos)
        if isinstance(end_pos, int):
            self.set_position(end_pos, mode="keep")
        else:
            self.move_position(end_pos, mode="keep")
        return self.selectedText()

    def replace_text(
        self,
        start_pos: int,
        end_pos: MoveOperationStr | int,
        to_replace: str,
    ):
        self.set_position(start_pos)
        if isinstance(end_pos, int):
            self.set_position(end_pos, mode="keep")
        else:
            self.move_position(end_pos, mode="keep")
        self.insertText(to_replace)
        self.select_text(start_pos, start_pos + len(to_replace))

    @contextlib.contextmanager
    def edit_block(self):
        """Context manager for edit blocks. Can be used for undo actions."""
        self.beginEditBlock()
        yield
        self.endEditBlock()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PlainTextEdit()
    widget.show()
    app.main_loop()
    cursor = widget.get_text_cursor()
    print(str(cursor))
