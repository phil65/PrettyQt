from __future__ import annotations

import contextlib

from typing import Literal

from prettyqt import gui
from prettyqt.utils import bidict


MOVE_MODE = bidict(
    move=gui.QTextCursor.MoveMode.MoveAnchor, keep=gui.QTextCursor.MoveMode.KeepAnchor
)

MoveModeStr = Literal["move", "keep"]

MOVE_OPERATION = bidict(
    no_move=gui.QTextCursor.MoveOperation.NoMove,
    start=gui.QTextCursor.MoveOperation.Start,
    start_of_line=gui.QTextCursor.MoveOperation.StartOfLine,
    start_of_block=gui.QTextCursor.MoveOperation.StartOfBlock,
    start_of_word=gui.QTextCursor.MoveOperation.StartOfWord,
    previous_block=gui.QTextCursor.MoveOperation.PreviousBlock,
    previous_char=gui.QTextCursor.MoveOperation.PreviousCharacter,
    previous_word=gui.QTextCursor.MoveOperation.PreviousWord,
    up=gui.QTextCursor.MoveOperation.Up,
    left=gui.QTextCursor.MoveOperation.Left,
    word_left=gui.QTextCursor.MoveOperation.WordLeft,
    end=gui.QTextCursor.MoveOperation.End,
    end_of_line=gui.QTextCursor.MoveOperation.EndOfLine,
    end_of_word=gui.QTextCursor.MoveOperation.EndOfWord,
    end_of_block=gui.QTextCursor.MoveOperation.EndOfBlock,
    next_block=gui.QTextCursor.MoveOperation.NextBlock,
    next_char=gui.QTextCursor.MoveOperation.NextCharacter,
    next_word=gui.QTextCursor.MoveOperation.NextWord,
    down=gui.QTextCursor.MoveOperation.Down,
    right=gui.QTextCursor.MoveOperation.Right,
    word_right=gui.QTextCursor.MoveOperation.WordRight,
    next_cell=gui.QTextCursor.MoveOperation.NextCell,
    previous_cell=gui.QTextCursor.MoveOperation.PreviousCell,
    next_row=gui.QTextCursor.MoveOperation.NextRow,
    previous_row=gui.QTextCursor.MoveOperation.PreviousRow,
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
    document=gui.QTextCursor.SelectionType.Document,
    block_under_cursor=gui.QTextCursor.SelectionType.BlockUnderCursor,
    line_under_cursor=gui.QTextCursor.SelectionType.LineUnderCursor,
    word_under_cursor=gui.QTextCursor.SelectionType.WordUnderCursor,
)

SelectionTypeStr = Literal[
    "document", "block_under_cursor", "line_under_cursor", "word_under_cursor"
]


class TextCursor(gui.QTextCursor):
    def __str__(self):
        return self.selectedText().replace("\u2029", "\n")

    def __contains__(self, other):
        return (
            self.selectionStart() <= other.selectionStart()
            and self.selectionEnd() >= other.selectionEnd()
        )

    def move_position(
        self, operation: MoveOperationStr, mode: MoveModeStr = "move", n: int = 1
    ) -> bool:
        if n < 0:
            raise ValueError(n)
        return self.movePosition(MOVE_OPERATION[operation], MOVE_MODE[mode], n)

    def set_position(self, pos: int | tuple[int, int], mode: MoveModeStr = "move"):
        """Set cursor to given position.

        0-indexed.

        Args:
            pos: Cursor position
            mode: Move mode
        """
        match pos:
            case int():
                self.setPosition(pos, MOVE_MODE[mode])
            case (int() as row, int() as col):
                position = self.document().find_block_by_number(row).position()
                position += col
                self.set_position(position, mode=mode)
            case _:
                raise TypeError(pos)

    def select(self, selection: SelectionTypeStr | gui.QTextCursor.SelectionType):
        if isinstance(selection, gui.QTextCursor.SelectionType):
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
        return (self.blockNumber(), self.positionInBlock())

    def get_selection(self) -> gui.TextDocumentFragment:
        return gui.TextDocumentFragment(self.selection())

    def select_text(
        self,
        start_pos: int | tuple[int, int] | MoveOperationStr,
        end_pos: int | tuple[int, int] | MoveOperationStr,
    ) -> str:
        """Select text from start position to end position.

        Positions can be either an integer index or a move operation

        Args:
            start_pos: Start position
            end_pos: End position
        """
        match start_pos:
            case int() | (int(), int()):
                self.set_position(start_pos)
            case str():
                self.move_position(start_pos)
            case _:
                raise TypeError(start_pos)
        match end_pos:
            case int() | (int(), int()):
                self.set_position(end_pos, mode="keep")
            case str():
                self.move_position(end_pos, mode="keep")
            case _:
                raise TypeError(end_pos)
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
    def edit_block(self, join_previous: bool = False):
        """Context manager for edit blocks. Can be used for undo actions."""
        self.joinPreviousEditBlock() if join_previous else self.beginEditBlock()
        yield
        self.endEditBlock()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PlainTextEdit()
    widget.show()
    app.exec()
    cursor = widget.selecter.get_text_cursor()
    print(cursor)
