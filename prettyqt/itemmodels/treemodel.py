from __future__ import annotations

import logging

from prettyqt import core
from prettyqt.utils import node


logger = logging.getLogger(__name__)


class TreeItem(node.Node):
    """Tree node class used for Qt TreeModels."""

    # __slots__ = ("has_children", "children_fetched")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_children = True
        self.children_fetched = False


class TreeModel(core.AbstractItemModel):
    """TreeModel which is used as a base for most TreeModels implemented.

    Tree gets dynamically populated whenever the the indexes get "expanded".

    basically, only 2 methods need to be defined in order to build the tree:

    def _fetch_object_children(self, TreeModel.TreeItem) -> list[TreeModel.TreeItem]:
        ...

    def _has_children(self, TreeModel.TreeItem) -> bool:
        ...

    Subclasses can override TreeModel.TreeItem if a child TreeItem class should be used
    for the root.

    """

    TreeItem = TreeItem

    def __init__(self, obj=None, show_root: bool = True, **kwargs):
        super().__init__(**kwargs)
        self._show_root = show_root
        self._root_item = self.TreeItem(obj=None)
        self.inspected_item = self._root_item
        self._init_root_item(obj)

    @property
    def show_root(self) -> bool:
        """Return True if the inspected node is visible.

        In that case an invisible root node has been added.
        """
        return self._show_root

    def _init_root_item(self, obj):
        if self._show_root:
            self._root_item = self.TreeItem(obj=None)
            self._root_item.children_fetched = True
            self.inspected_item = self.TreeItem(obj=obj)
            self._root_item.append_child(self.inspected_item)
        else:
            # The root itself will be invisible
            self._root_item = self.TreeItem(obj=obj)
            self.inspected_item = self._root_item
            self._fetch_children(self._root_item)

    def set_root_item(self, obj):
        """Set a new object to display. Resets the model."""
        with self.reset_model():
            self._init_root_item(obj)

    @property
    def root_item(self) -> TreeModel.TreeItem:
        return self._root_item

    def data_by_index(self, index: core.ModelIndex) -> TreeModel.TreeItem:
        return index.internalPointer() if index.isValid() else self.root_item

    def index_for_item(
        self, item: TreeModel.TreeItem, column: int = 0
    ) -> core.ModelIndex:
        if item is self.root_item or item.parent_item is None:
            return core.ModelIndex()
        return self.createIndex(item.row(), column, item)

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        if not self.hasIndex(row, column, parent):
            return core.ModelIndex()
        parent_item = self.data_by_index(parent)
        child_item = parent_item.children[row]
        return self.createIndex(row, column, child_item)

    def parent(self, index: core.ModelIndex | None = None) -> core.ModelIndex:
        # hacky way to let the case without any arguments get through.
        # not really nice, a proper dispatch library would be better.
        # functools.singledispatchmethod doesnt work here.
        index = index or core.ModelIndex()
        if not index.isValid():
            return core.ModelIndex()

        child_item = self.data_by_index(index)
        parent_item = child_item.parent_item

        if parent_item is None or parent_item is self.root_item:
            return core.ModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 else len(self.data_by_index(parent).children)

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        treeitem = self.data_by_index(parent)
        if treeitem.children_fetched:
            return len(treeitem.children) > 0
        if self._show_root and treeitem is self._root_item:
            return True
        return bool(self._has_children(treeitem))

    def canFetchMore(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
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
        if not tree_items:
            parent_item.children_fetched = True
            return
        first = len(parent_item.children)
        with self.insert_rows(first, first + len(tree_items) - 1, parent):
            self._add_fetched_children(parent_item, tree_items)

    def _fetch_children(self, parent_item: TreeModel.TreeItem):
        """Fetch children without emitting signals (used during reset)."""
        if not parent_item.children_fetched:
            items = self._fetch_object_children(parent_item)
            self._add_fetched_children(parent_item, items)

    @staticmethod
    def _add_fetched_children(parent_item: TreeModel.TreeItem, items):
        for tree_item in items:
            parent_item.append_child(tree_item)
        parent_item.children_fetched = True

    def _fetch_object_children(self, treeitem) -> list[TreeModel.TreeItem]:
        return []

    def _has_children(self, treeitem) -> bool:
        return treeitem.has_children


if __name__ == "__main__":
    model = TreeModel("test")
    model.parent()
