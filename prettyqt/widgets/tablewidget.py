from typing import Tuple

from qtpy import QtCore, QtWidgets

from prettyqt import widgets


QtWidgets.QTableWidget.__bases__ = (widgets.TableView,)


class TableWidget(QtWidgets.QTableWidget):
    def __getitem__(self, index: Tuple[int, int]) -> QtWidgets.QTableWidgetItem:
        return self.item(*index)

    def __setitem__(self, index: Tuple[int, int], value: QtWidgets.QTableWidgetItem):
        self.setItem(index[0], index[1], value)

    def __delitem__(self, index: Tuple[int, int]):
        self.takeItem(*index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(column, order)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TableWidget()
    widget.setHorizontalHeaderLabels(["testus"])
    widget.setColumnCount(1)
    widget.insertRow(0)
    widget[0, 0] = widgets.TableWidgetItem("test")
    widget.show()
    app.main_loop()
