# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets


QtWidgets.QTableWidget.__bases__ = (widgets.TableView,)


class TableWidget(QtWidgets.QTableWidget):
    def sort(self, column=0, reverse=False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(column, order)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TableWidget()
    widget.show()
    app.exec_()
