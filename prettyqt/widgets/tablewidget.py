# -*- coding: utf-8 -*-

from qtpy import QtCore, QtWidgets

from prettyqt import widgets


QtWidgets.QTableWidget.__bases__ = (widgets.TableView,)


class TableWidget(QtWidgets.QTableWidget):
    def sort(self, column=0, reverse=False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(column, order)

    def __getitem__(self, index):
        return self.item(*index)

    def __setitem__(self, index, value):
        print(index, value)
        self.setItem(index[0], index[1], value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TableWidget()
    widget.setHorizontalHeaderLabels(["testus"])
    widget.setColumnCount(1)
    widget.insertRow(0)
    widget[0, 0] = widgets.TableWidgetItem("test")
    widget.show()
    app.main_loop()
