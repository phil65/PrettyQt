from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class TreeWidgetMixin:
    def __contains__(self, other: QtWidgets.QTreeWidgetItem):
        return self.indexOfTopLevelItem(other) >= 0

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)


class TreeWidget(TreeWidgetMixin, QtWidgets.QTreeWidget, widgets.TreeView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = TreeWidget()
    widget.show()
    app.main_loop()
