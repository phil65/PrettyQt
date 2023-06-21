from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import listdelegators, InvalidParamError


class TreeWidgetMixin(widgets.TreeViewMixin):
    def __contains__(self, other: QtWidgets.QTreeWidgetItem):
        return self.indexOfTopLevelItem(other) >= 0

    def __getitem__(
        self, index: int | slice
    ) -> (
        QtWidgets.QTreeWidgetItem
        | listdelegators.BaseListDelegator[QtWidgets.QTreeWidgetItem]
    ):
        match index:
            case int():
                item = self.topLevelItem(index)
                if item is None:
                    raise KeyError(index)
                return item
            case slice():
                count = self.topLevelItemCount() if index.stop is None else index.stop
                values = list(range(count)[index])
                ls = [self.topLevelItem(i) for i in values]
                return listdelegators.BaseListDelegator(ls)
            case _:
                raise TypeError(index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)

    def find_items(
        self,
        text: str,
        column: int = 0,
        mode: constants.MatchFlagStr = "exact",
        recursive: bool = False,
        case_sensitive: bool = False,
    ) -> listdelegators.BaseListDelegator[QtWidgets.QTreeWidgetItem]:
        if mode not in constants.MATCH_FLAGS:
            raise InvalidParamError(mode, constants.MATCH_FLAGS)
        flag = constants.MATCH_FLAGS[mode]
        if recursive:
            flag |= QtCore.Qt.MatchFlag.MatchRecursive
        if case_sensitive:
            flag |= QtCore.Qt.MatchFlag.MatchCaseSensitive
        items = self.findItems(text, flag, column)
        return listdelegators.BaseListDelegator(items)

    def get_items(
        self, recursive: bool = False
    ) -> listdelegators.BaseListDelegator[QtWidgets.QTreeWidgetItem]:
        """Get TreeWidgetItems of this widget.

        Arguments:
            recursive: whether to include all items of the tree.

        recursive option is written iteratively to also support original QTreeWidgetItems.
        """
        root = self.invisibleRootItem(())
        if not recursive:
            return [root.child(i) for i in range(root.childCount())]
        results = []
        nodes = [root]
        while nodes:
            items = []
            for node in nodes:
                results.append(node)
                items.extend(node.child(i) for i in range(node.childCount()))
            nodes = items
        return listdelegators.BaseListDelegator(results[1:])

    def scroll_to_item(
        self,
        item: QtWidgets.QTreeWidgetItem,
        scroll_hint: widgets.abstractitemview.ScrollHintStr = "ensure_visible",
    ):
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT[scroll_hint])

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
    app.exec()
