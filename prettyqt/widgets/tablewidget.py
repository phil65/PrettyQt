from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QTableWidget.__bases__ = (widgets.TableView,)


class TableWidget(QtWidgets.QTableWidget):
    def __getitem__(self, index: tuple[int, int]) -> QtWidgets.QTableWidgetItem:
        item = self.item(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __setitem__(self, index: tuple[int, int], value: QtWidgets.QTableWidgetItem):
        self.setItem(index[0], index[1], value)

    def __delitem__(self, index: tuple[int, int]):
        self.takeItem(*index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
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
