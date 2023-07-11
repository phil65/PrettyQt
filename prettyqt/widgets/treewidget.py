from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.utils import listdelegators


class TreeWidgetMixin(widgets.TreeViewMixin):
    def __contains__(self, other: widgets.QTreeWidgetItem):
        return self.indexOfTopLevelItem(other) >= 0

    def __getitem__(
        self, index: int | slice
    ) -> widgets.QTreeWidgetItem | listdelegators.ListDelegator[widgets.QTreeWidgetItem]:
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
                return listdelegators.ListDelegator(ls)
            case _:
                raise TypeError(index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)

    def find_items(
        self,
        text: str,
        column: int = 0,
        mode: constants.MatchFlagStr | constants.MatchFlag = "exact",
        recursive: bool = False,
        case_sensitive: bool = False,
    ) -> listdelegators.ListDelegator[widgets.QTreeWidgetItem]:
        flag = constants.MATCH_FLAGS.get_enum_value(mode)
        if recursive:
            flag |= constants.MatchFlag.MatchRecursive
        if case_sensitive:
            flag |= constants.MatchFlag.MatchCaseSensitive
        items = self.findItems(text, flag, column)
        return listdelegators.ListDelegator(items)

    def get_items(
        self, recursive: bool = False
    ) -> listdelegators.ListDelegator[widgets.QTreeWidgetItem]:
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
        return listdelegators.ListDelegator(results[1:])

    def scroll_to_item(
        self,
        item: widgets.QTreeWidgetItem,
        scroll_hint: widgets.abstractitemview.ScrollHintStr
        | widgets.QAbstractItemView.ScrollHint = "ensure_visible",
    ):
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT[scroll_hint])

    def removeTopLevelItem(self, item):
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i) is item:
                self.takeTopLevelItem(i)
                return
        raise IndexError(f"Item {item!r} not in top-level items.")

    def openPersistentEditor(
        self, index: core.ModelIndex | widgets.QTreeWidgetItem, column: int = 0
    ):
        if isinstance(index, core.ModelIndex):
            column = index.column()
            index = self.itemFromIndex(index)
        super().openPersistentEditor(index, column)

    def closePersistentEditor(
        self, index: core.ModelIndex | widgets.QTreeWidgetItem, column: int = 0
    ):
        if isinstance(index, core.ModelIndex):
            column = index.column()
            index = self.itemFromIndex(index)
        super().closePersistentEditor(index, column)

    def isPersistentEditorOpen(
        self, index: core.ModelIndex | widgets.QTreeWidgetItem, column: int = 0
    ) -> bool:
        if isinstance(index, core.ModelIndex):
            column = index.column()
            index = self.itemFromIndex(index)
        return super().isPersistentEditorOpen(index, column)


class TreeWidget(TreeWidgetMixin, widgets.QTreeWidget):
    """Tree view that uses a predefined tree model."""


if __name__ == "__main__":
    app = widgets.app()
    widget = TreeWidget()
    widget.openPersistentEditor(core.ModelIndex(), 1)
    widget.show()
    app.exec()
