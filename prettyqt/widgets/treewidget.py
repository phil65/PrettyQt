from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class TreeWidgetMixin(widgets.TreeViewMixin):
    def __contains__(self, other: QtWidgets.QTreeWidgetItem):
        return self.indexOfTopLevelItem(other) >= 0

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)

    def collapse_tree(self, item):
        item.setExpanded(False)
        for i in range(item.childCount()):
            self.collapse_tree(item.child(i))

    def removeTopLevelItem(self, item):
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i) is item:
                self.takeTopLevelItem(i)
                return
        raise IndexError(f"Item '{str(item)}' not in top-level items.")

    def openPersistentEditor(
        self, index: QtCore.QModelIndex | QtWidgets.QTreeWidgetItem, column: int = 0
    ):
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
            column = index.column()
        super().openPersistentEditor(index, column)

    def closePersistentEditor(
        self, index: QtCore.QModelIndex | QtWidgets.QTreeWidgetItem, column: int = 0
    ):
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
            column = index.column()
        super().closePersistentEditor(index, column)

    def isPersistentEditorOpen(
        self, index: QtCore.QModelIndex | QtWidgets.QTreeWidgetItem, column: int = 0
    ) -> bool:
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
            column = index.column()
        return super().isPersistentEditorOpen(index, column)


class TreeWidget(TreeWidgetMixin, QtWidgets.QTreeWidget):
    pass


if __name__ == "__main__":
    from prettyqt.qt import QtCore

    app = widgets.app()
    widget = TreeWidget()
    widget.openPersistentEditor(QtCore.QModelIndex(), 1)
    widget.show()
    app.main_loop()
