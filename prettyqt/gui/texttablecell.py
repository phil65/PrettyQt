from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class TextTableCell(QtGui.QTextTableCell):
    def get_format(self) -> gui.TextCharFormat:
        #  .format() seems to crash both bindings?
        return gui.TextCharFormat(self.format())

    def get_first_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.firstCursorPosition())

    def get_last_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.lastCursorPosition())


if __name__ == "__main__":
    app = gui.app()
    cell = TextTableCell()
    cell.get_format()
