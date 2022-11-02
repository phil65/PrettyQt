# Based on: PySide examples/itemviews/simpletreemodel
# See: http://harmattan-dev.nokia.com/docs/library/html/qt4/itemviews-simpletreemodel.html

from __future__ import annotations

from collections.abc import Sequence
import logging
from typing import Generic, TypeVar

from prettyqt.utils import helpers


logger = logging.getLogger(__name__)

MAX_OBJ_STR_LEN = 50

T = TypeVar("T", bound="TreeItem")  # Declare type variable


class TreeItem(Generic[T]):
    """Tree node class that can be used to build trees of objects."""

    def __init__(self, obj, parent: T | None = None):
        self.parent_item = parent
        self.obj = obj
        self.child_items: list[T] = []
        self.has_children = True
        self.children_fetched = False

    def __repr__(self):
        name = type(self).__name__
        if len(self.child_items) == 0:
            string = helpers.cut_off_str(self.obj, MAX_OBJ_STR_LEN)
            return f"<{name}(0x{id(self.obj):x}): = {string}>"
        else:
            n = len(self.child_items)
            return f"<{name}(0x{id(self.obj):x}): ({n:d} children)>"

    def append_child(self, item: T):
        item.parent_item = self
        self.child_items.append(item)

    def insert_children(self, idx: int, items: Sequence[T]):
        self.child_items[idx:idx] = items
        for item in items:
            item.parent_item = self

    def child(self, row: int) -> T:
        return self.child_items[row]

    def child_count(self) -> int:
        return len(self.child_items)

    def parent(self) -> T | None:
        return self.parent_item

    def row(self) -> int:
        return self.parent_item.child_items.index(self) if self.parent_item else 0

    def pretty_print(self, indent: int = 0):
        logger.debug(indent * "    " + str(self))
        for child_item in self.child_items:
            child_item.pretty_print(indent + 1)
