from __future__ import annotations

from prettyqt import core
from prettyqt.utils import treeitem


class TreeModel(core.AbstractItemModel):
    TreeItem = treeitem.TreeItem

    def __init__(self, obj=None, show_root: bool = True, **kwargs):
        super().__init__(**kwargs)
        self._root_item = treeitem.TreeItem(obj=obj)
        self._show_root = show_root
        self.set_root_item(obj)

    @property
    def show_root(self) -> bool:
        """Return True if the inspected node is visible.

        In that case an invisible root node has been added.
        """
        return self._show_root

    def set_root_item(self, obj):
        if self._show_root:
            self._root_item = self.TreeItem(obj=None)
            self._root_item.children_fetched = True
            self.inspected_item = self.TreeItem(obj=obj)
            self._root_item.append_child(self.inspected_item)
            # root_index = self.index(0, 0)
            # self.fetchMore(self.index(0, 0, root_index))
        else:
            # The root itself will be invisible
            self._root_item = self.TreeItem(obj=obj)
            self.inspected_item = self._root_item
            root_index = self.index(0, 0)
            self.fetchMore(root_index)

    @property
    def root_item(self) -> treeitem.TreeItem:
        """Return the root ObjectBrowserTreeItem."""
        return self._root_item

    def data_by_index(self, index: core.ModelIndex) -> treeitem.TreeItem:
        return index.internalPointer() if index.isValid() else self.root_item

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        parent_item = self.data_by_index(parent)

        if not self.hasIndex(row, column, parent):
            return core.ModelIndex()

        if child_item := parent_item.child(row):  # isnt this always true?
            return self.createIndex(row, column, child_item)
        return core.ModelIndex()

    def parent(self, index: core.ModelIndex | None = None) -> core.ModelIndex:
        # hacky way to let the case without any arguments get through.
        # not really nice, a proper dispatch library would be better.
        # functools.singledispatchmethod doesnt work here.
        if index is None:
            return super().parent()
        if not index.isValid():
            return core.ModelIndex()

        child_item = self.data_by_index(index)
        parent_item = child_item.parent()

        if parent_item is None or parent_item == self.root_item:
            return core.ModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: core.ModelIndex | None = None):
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 else self.data_by_index(parent).child_count()

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 else self.data_by_index(parent).has_children

    def canFetchMore(self, parent: core.ModelIndex | None = None):
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        else:
            return not self.data_by_index(parent).children_fetched

    def fetchMore(self, parent: core.ModelIndex | None = None):
        """Fetch the children given the model index of a parent node.

        Adds the children to the parent.
        """
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return

        parent_item = self.data_by_index(parent)
        if parent_item.children_fetched:
            return

        tree_items = self._fetch_object_children(parent_item)

        with self.insert_rows(0, len(tree_items) - 1, parent):
            for tree_item in tree_items:
                parent_item.append_child(tree_item)
            parent_item.children_fetched = True

    def _fetch_object_children(self, treeitem) -> list[treeitem.TreeItem]:
        return NotImplemented


if __name__ == "__main__":
    model = TreeModel("test")
    model.parent()
