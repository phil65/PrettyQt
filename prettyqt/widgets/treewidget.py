from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets


QtWidgets.QTreeWidget.__bases__ = (widgets.TreeView,)


class TreeWidget(QtWidgets.QTreeWidget):
    def __contains__(self, other: QtWidgets.QTreeWidgetItem):
        return self.indexOfTopLevelItem(other) >= 0

    def sort(self, column: int = 0, reverse: bool = False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(column, order)


if __name__ == "__main__":
    app = widgets.app()
    widget = TreeWidget()
    widget.show()
    app.main_loop()
