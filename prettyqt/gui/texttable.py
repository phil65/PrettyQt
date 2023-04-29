from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class TextTable(gui.textframe.TextFrameMixin, QtGui.QTextTable):
    def __getitem__(self, index: int | tuple[int, int]) -> gui.TextTableCell:
        if isinstance(index, int):
            cell = gui.TextTableCell(self.cellAt(index))
        else:
            cell = gui.TextTableCell(self.cellAt(*index))
        if not cell.isValid():
            raise IndexError(index)
        return cell

    # def get_format(self) -> gui.TextTableFormat:
    #     return gui.TextTableFormat(self.format())


if __name__ == "__main__":
    doc = gui.TextDocument()
    table = TextTable(doc)
