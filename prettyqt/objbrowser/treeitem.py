# Based on: PySide examples/itemviews/simpletreemodel
# See: http://harmattan-dev.nokia.com/docs/library/html/qt4/itemviews-simpletreemodel.html

# Disabling the need for docstrings, all methods are tiny.
# pylint: disable=C0111

import logging

from prettyqt.utils import helpers

logger = logging.getLogger(__name__)

MAX_OBJ_STR_LEN = 50


def name_is_special(method_name):
    """Returns true if the method name starts and ends with two underscores."""
    return method_name.startswith("__") and method_name.endswith("__")


class TreeItem(object):
    """Tree node class that can be used to build trees of objects."""

    def __init__(self, obj, name, obj_path, is_attribute, parent=None):
        self.parent_item = parent
        self.obj = obj
        self.obj_name = str(name)
        self.obj_path = str(obj_path)
        self.is_attribute = is_attribute
        self.child_items = []
        self.has_children = True
        self.children_fetched = False

    def __repr__(self):
        if len(self.child_items) == 0:
            string = helpers.cut_off_str(self.obj, MAX_OBJ_STR_LEN)
            return f"<TreeItem(0x{id(self.obj):x}): {self.obj_path} = {string}>"
        else:
            n = len(self.child_items)
            return f"<TreeItem(0x{id(self.obj):x}): {self.obj_path} ({n:d} children)>"

    @property
    def is_special_attribute(self) -> bool:
        """Return true if the item represents a dunder attribute."""
        return self.is_attribute and name_is_special(self.obj_name)

    @property
    def is_callable_attribute(self) -> bool:
        """Return true if the items is an attribute and it is callable."""
        return self.is_attribute and callable(self.obj)

    def append_child(self, item):
        item.parent_item = self
        self.child_items.append(item)

    def insert_children(self, idx: int, items):
        self.child_items[idx:idx] = items
        for item in items:
            item.parent_item = self

    def child(self, row: int):
        return self.child_items[row]

    def child_count(self) -> int:
        return len(self.child_items)

    def parent(self):
        return self.parent_item

    def row(self) -> int:
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        else:
            return 0

    def pretty_print(self, indent=0):
        logger.debug(indent * "    " + str(self))
        for child_item in self.child_items:
            child_item.pretty_print(indent + 1)
