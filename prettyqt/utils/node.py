from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Self

from prettyqt.utils import baseresolver, get_repr


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, Sequence


logger = logging.getLogger(__name__)


class NodeResolver(baseresolver.BaseResolver):
    def __init__(self, path_attr: str = "obj", ignore_case: bool = False):
        """Resolve any `Node` paths using attribute `path_attr`.

        Arguments:
            path_attr: Name of the node attribute to be used for resolving
            ignore_case: Enable case insensisitve handling.
        """
        super().__init__(ignore_case=ignore_case)
        self.path_attr = path_attr

    def get_parent(self, node):
        return node.parent

    def get_children(self, node):
        return node.children

    def get_root(self, node):
        return node.root

    def get_attribute(self, node):
        return getattr(node, self.path_attr)


class BaseNode:
    """A Node class that can be used to build trees."""

    # __slots__ = ("parent_item", "children")

    def __init__(self, parent: Self | None = None):
        self.parent_item = parent
        self.children: list[Self] = []

    def __repr__(self):
        return get_repr(self)

    def __iter__(self) -> Iterator[Self]:
        return iter(self.children)

    def __getitem__(self, index: int) -> Self:
        return self.children[index]

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
            return None
        return None

    @property
    def right_sibling(self) -> Self | None:
        """Get sibling right of self."""
        if self.parent_item:
            children = self.parent_item.children
            child_idx = children.index(self)
            if child_idx + 1 < len(children):
                return self.parent_item.children[child_idx + 1]
            return None
        return None

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
        text = indent * "    " + repr(self)
        logger.info(text)
        for child_item in self.children:
            child_item.pretty_print(indent + 1)


class Node(BaseNode):
    """Like BaseNode, but with one object attached to the node."""

    # __slots__ = ("obj",)

    def __init__(self, obj, parent: Self | None = None):
        super().__init__(parent)
        self.obj = obj

    def __repr__(self):
        return get_repr(self, self.obj)


def preorder_iter(
    tree: BaseNode,
    filter_condition: Callable[[BaseNode], bool] | None = None,
    stop_condition: Callable[[BaseNode], bool] | None = None,
    max_depth: int = 0,
) -> Iterable[BaseNode]:
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
    if (not max_depth or tree.depth <= max_depth) and (
        not stop_condition or not stop_condition(tree)
    ):
        if not filter_condition or filter_condition(tree):
            yield tree
        for child in tree.children:
            yield from preorder_iter(child, filter_condition, stop_condition, max_depth)


if __name__ == "__main__":
    model = Node("test")
    model.parent()
