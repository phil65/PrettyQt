from __future__ import annotations

from typing import Tuple

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets


QtWidgets.QTableWidget.__bases__ = (widgets.TableView,)


class TableWidget(QtWidgets.QTableWidget):
    def __getitem__(self, index: Tuple[int, int]) -> QtWidgets.QTableWidgetItem:
        item = self.item(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __setitem__(self, index: Tuple[int, int], value: QtWidgets.QTableWidgetItem):
        self.setItem(index[0], index[1], value)

    def __delitem__(self, index: Tuple[int, int]):
        self.takeItem(*index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(column, order)


if __name__ == "__main__":
    app = widgets.app()
    widget = TableWidget()
    widget.setHorizontalHeaderLabels(["testus"])
    widget.setColumnCount(1)
    widget.insertRow(0)
    widget[0, 0] = widgets.TableWidgetItem("test")
    widget.show()
    app.main_loop()
