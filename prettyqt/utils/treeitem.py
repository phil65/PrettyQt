# Based on: PySide examples/itemviews/simpletreemodel
# See: http://harmattan-dev.nokia.com/docs/library/html/qt4/itemviews-simpletreemodel.html

from __future__ import annotations

from collections.abc import Iterator, Sequence
import logging

from typing_extensions import Self

from prettyqt.utils import get_repr


logger = logging.getLogger(__name__)

MAX_OBJ_STR_LEN = 50


class TreeItem:
    """Tree node class that can be used to build trees of objects."""

    __slots__ = ("parent_item", "obj", "child_items", "has_children", "children_fetched")

    def __init__(self, obj, parent: Self | None = None):
        self.parent_item = parent
        self.obj = obj
        self.child_items: list[Self] = []
        self.has_children = True
        self.children_fetched = False

    def __repr__(self):
        return get_repr(self, self.obj)

    def __iter__(self) -> Iterator[Self]:
        return iter(self.child_items)

    def append_child(self, item: Self):
        item.parent_item = self
        self.child_items.append(item)

    def insert_children(self, idx: int, items: Sequence[Self]):
        self.child_items[idx:idx] = items
        for item in items:
            item.parent_item = self

    def child(self, row: int) -> Self:
        return self.child_items[row]

    def child_count(self) -> int:
        return len(self.child_items)

    def parent(self) -> Self | None:
        return self.parent_item

    def row(self) -> int:
        return self.parent_item.child_items.index(self) if self.parent_item else 0

    def pretty_print(self, indent: int = 0):
        text = indent * "    " + str(self)
        logger.debug(text)
        for child_item in self.child_items:
            child_item.pretty_print(indent + 1)


if __name__ == "__main__":
    t = TreeItem(None)
    print(t)
