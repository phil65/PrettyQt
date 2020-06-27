# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt.utils import bidict


MOVE_MODES = bidict(move=QtGui.QTextCursor.MoveAnchor,
                    keep=QtGui.QTextCursor.KeepAnchor)

MOVE_OPERATIONS = bidict(no_move=QtGui.QTextCursor.NoMove,
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
                         previous_row=QtGui.QTextCursor.PreviousRow)

SELECTION_TYPES = bidict(document=QtGui.QTextCursor.Document,
                         block_under_cursor=QtGui.QTextCursor.BlockUnderCursor,
                         line_under_cursor=QtGui.QTextCursor.LineUnderCursor,
                         word_under_cursor=QtGui.QTextCursor.WordUnderCursor)


class TextCursor(QtGui.QTextCursor):

    def move_position(self, operation: str, mode: str = "move", n: int = 1) -> bool:
        op = MOVE_OPERATIONS[operation]
        mode = MOVE_MODES[mode]
        return self.movePosition(op, mode, n)

    def set_position(self, pos: int, mode: str = "move"):
        """set cursor to given position

        Args:
            pos: Cursor position
            mode: Move mode (default: {"move"})
        """
        self.setPosition(pos, MOVE_MODES[mode])

    def select(self, selection):
        if selection in SELECTION_TYPES:
            selection = SELECTION_TYPES[selection]
        super().select(selection)

    def select_text(self, start_pos: int, end_pos: int):
        """select text from start position to end position

        Args:
            start_pos: Start position
            end_pos: End position
        """
        self.set_position(start_pos)
        self.set_position(end_pos, mode="keep")
