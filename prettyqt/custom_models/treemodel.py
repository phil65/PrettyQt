from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
import logging

from typing_extensions import Self

from prettyqt import core
from prettyqt.utils import get_repr


logger = logging.getLogger(__name__)


class TreeItem:
    """Tree node class that can be used to build trees of objects."""

    __slots__ = ("parent_item", "obj", "children", "has_children", "children_fetched")

    def __init__(self, obj, parent: Self | None = None):
        self.parent_item = parent
        self.obj = obj
        self.children: list[Self] = []
        self.has_children = True
        self.children_fetched = False

    def __repr__(self):
        return get_repr(self, self.obj)

    def __iter__(self) -> Iterator[Self]:
        return iter(self.children)

    def __getitem__(self, index: int) -> Self:
        return self.child(index)

    def __rshift__(self, other: Self):
        """Set children using >> bitshift operator for self >> other.

        Args:
            other (Self): other node, children
        """
        other.parent_item = self

    def __lshift__(self, other: Self):
        """Set parent using << bitshift operator for self << other.

        Args:
            other (Self): other node, parent
        """
        self.parent_item = other

    def __copy__(self) -> Self:
        """Shallow copy self."""
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def append_child(self, item: Self):
        item.parent_item = self
        self.children.append(item)

    def insert_children(self, idx: int, items: Sequence[Self]):
        self.children[idx:idx] = items
        for item in items:
            item.parent_item = self

    def child(self, row: int) -> Self:
        return self.children[row]

    def child_count(self) -> int:
        return len(self.children)

    def parent(self) -> Self | None:
        return self.parent_item

    @property
    def ancestors(self) -> Iterable[Self]:
        """Get iterator to yield all ancestors of self, does not include self."""
        node = self
        while (node := node.parent_item) is not None:
            yield node

    @property
    def descendants(self) -> Iterable[Self]:
        """Get iterator to yield all descendants of self, does not include self."""
        yield from preorder_iter(self, filter_condition=lambda _node: _node != self)

    @property
    def leaves(self) -> Iterable[Self]:
        """Get iterator to yield all leaf nodes from self."""
        yield from preorder_iter(self, filter_condition=lambda _node: _node.is_leaf)

    @property
    def siblings(self) -> Iterable[Self]:
        """Get siblings of self."""
        if self.parent_item is None:
            return ()
        return tuple(child for child in self.parent_item.children if child is not self)

    @property
    def left_sibling(self) -> Self | None:
        """Get sibling left of self."""
        if self.parent_item:
            children = self.parent_item.children
            if child_idx := children.index(self):
                return self.parent_item.children[child_idx - 1]

    @property
    def right_sibling(self) -> Self | None:
        """Get sibling right of self."""
        if self.parent_item:
            children = self.parent_item.children
            child_idx = children.index(self)
            if child_idx + 1 < len(children):
                return self.parent_item.children[child_idx + 1]

    @property
    def node_path(self) -> Iterable[Self]:
        """Get tuple of nodes starting from root."""
        if self.parent_item is None:
            return [self]
        return (*list(self.parent_item.node_path), self)

    @property
    def is_root(self) -> bool:
        """Get indicator if self is root node."""
        return self.parent_item is None

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node."""
        return not len(list(self.children))

    @property
    def root(self) -> Self:
        """Get root node of tree."""
        return self if self.parent_item is None else self.parent_item.root

    @property
    def depth(self) -> int:
        """Get depth of self, indexing starts from 1."""
        return 1 if self.parent_item is None else self.parent_item.depth + 1

    @property
    def max_depth(self) -> int:
        """Get maximum depth from root to leaf node."""
        return max(
            [self.root.depth] + [node.depth for node in list(self.root.descendants)]
        )

    def row(self) -> int:
        return self.parent_item.children.index(self) if self.parent_item else 0

    def pretty_print(self, indent: int = 0):
        text = indent * "    " + str(self)
        logger.debug(text)
        for child_item in self.children:
            child_item.pretty_print(indent + 1)


class TreeModel(core.AbstractItemModel):
    TreeItem = TreeItem

    def __init__(self, obj=None, show_root: bool = True, **kwargs):
        super().__init__(**kwargs)
        self._root_item = self.TreeItem(obj=obj)
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
    def root_item(self) -> TreeModel.TreeItem:
        return self._root_item

    def data_by_index(self, index: core.ModelIndex) -> TreeModel.TreeItem:
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
        index = index or core.ModelIndex()
        if not index.isValid():
            return core.ModelIndex()

        child_item = self.data_by_index(index)
        parent_item = child_item.parent()

        if parent_item is None or parent_item == self.root_item:
            return core.ModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 else len(self.data_by_index(parent).children)

    def hasChildren(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        treeitem = self.data_by_index(parent)
        if self._show_root and treeitem == self._root_item:
            return True
        return self._has_children(treeitem)

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

    def _fetch_object_children(self, treeitem) -> list[TreeModel.TreeItem]:
        return treeitem.children

    def _has_children(self, treeitem) -> bool:
        return treeitem.has_children


def preorder_iter(
    tree: TreeItem,
    filter_condition: Callable[[TreeItem], bool] | None = None,
    stop_condition: Callable[[TreeItem], bool] | None = None,
    max_depth: int = 0,
) -> Iterable[TreeItem]:
    """Iterate through all children of a tree.

    Pre-Order Iteration Algorithm, NLR
        1. Visit the current node.
        2. Recursively traverse the current node's left subtree.
        3. Recursively traverse the current node's right subtree.

    It is topologically sorted because a parent node is processed before its child nodes.

    >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    >>> [node.node_name for node in preorder_iter(root)]
    ['a', 'b', 'd', 'e', 'g', 'h', 'c', 'f']

    >>> [node.node_name for node in preorder_iter(root,
    filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
    ['a', 'd', 'e', 'g', 'f']

    >>> [node.node_name for node in preorder_iter(root,
    stop_condition=lambda x: x.node_name=="e")]
    ['a', 'b', 'd', 'c', 'f']

    >>> [node.node_name for node in preorder_iter(root, max_depth=3)]
    ['a', 'b', 'd', 'e', 'c', 'f']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument, optional
            Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument, optional
            Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute, optional
    """
    if (
        tree
        and (not max_depth or tree.depth <= max_depth)
        and (not stop_condition or not stop_condition(tree))
    ):
        if not filter_condition or filter_condition(tree):
            yield tree
        for child in tree.children:
            yield from preorder_iter(child, filter_condition, stop_condition, max_depth)


if __name__ == "__main__":
    model = TreeModel("test")
    model.parent()
