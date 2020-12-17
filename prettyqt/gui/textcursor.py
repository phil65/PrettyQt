import contextlib
from typing import Literal, Union

from qtpy import QtGui

from prettyqt.utils import bidict


MOVE_MODE = bidict(move=QtGui.QTextCursor.MoveAnchor, keep=QtGui.QTextCursor.KeepAnchor)

MoveModeStr = Literal["move", "keep"]

MOVE_OPERATION = bidict(
    no_move=QtGui.QTextCursor.NoMove,
    start=QtGui.QTextCursor.Start,
    start_of_line=QtGui.QTextCursor.StartOfLine,
    start_of_block=QtGui.QTextCursor.StartOfBlock,
    start_of_word=QtGui.QTextCursor.StartOfWord,
    previous_block=QtGui.QTextCursor.PreviousBlock,
    previous_char=QtGui.QTextCursor.PreviousCharacter,
    previous_word=QtGui.QTextCursor.PreviousWord,
    up=QtGui.QTextCursor.Up,
    left=QtGui.QTextCursor.Left,
    word_left=QtGui.QTextCursor.WordLeft,
    end=QtGui.QTextCursor.End,
    end_of_line=QtGui.QTextCursor.EndOfLine,
    end_of_word=QtGui.QTextCursor.EndOfWord,
    end_of_block=QtGui.QTextCursor.EndOfBlock,
    next_block=QtGui.QTextCursor.NextBlock,
    next_char=QtGui.QTextCursor.NextCharacter,
    next_word=QtGui.QTextCursor.NextWord,
    down=QtGui.QTextCursor.Down,
    right=QtGui.QTextCursor.Right,
    word_right=QtGui.QTextCursor.WordRight,
    next_cell=QtGui.QTextCursor.NextCell,
    previous_cell=QtGui.QTextCursor.PreviousCell,
    next_row=QtGui.QTextCursor.NextRow,
    previous_row=QtGui.QTextCursor.PreviousRow,
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
    document=QtGui.QTextCursor.Document,
    block_under_cursor=QtGui.QTextCursor.BlockUnderCursor,
    line_under_cursor=QtGui.QTextCursor.LineUnderCursor,
    word_under_cursor=QtGui.QTextCursor.WordUnderCursor,
)

SelectionTypeStr = Literal[
    "document", "block_under_cursor", "line_under_cursor", "word_under_cursor"
]


class TextCursor(QtGui.QTextCursor):
    def move_position(
        self, operation: MoveOperationStr, mode: MoveModeStr = "move", n: int = 1
    ) -> bool:
        op = MOVE_OPERATION[operation]
        mode = MOVE_MODE[mode]
        return self.movePosition(op, mode, n)

    def set_position(self, pos: int, mode: MoveModeStr = "move"):
        """Set cursor to given position.

        Args:
            pos: Cursor position
            mode: Move mode
        """
        self.setPosition(pos, MOVE_MODE[mode])

    def select(self, selection: SelectionTypeStr):
        if selection in SELECTION_TYPE:
            selection = SELECTION_TYPE[selection]
        super().select(selection)

    def span(self) -> tuple:
        return (self.anchor(), self.position())

    def select_text(
        self,
        start_pos: Union[int, MoveOperationStr],
        end_pos: Union[int, MoveOperationStr],
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
        end_pos: Union[MoveOperationStr, int],
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
