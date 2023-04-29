from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class TextTableCell(QtGui.QTextTableCell):
    def get_format(self) -> gui.TextCharFormat:
        return gui.TextCharFormat(self.format())


if __name__ == "__main__":
    app = gui.app()
    cell = TextTableCell()
    cell.get_format()
