"""Module that defines the TreeModel.

Based on: PySide examples/itemviews/simpletreemodel
See: https://github.com/PySide/Examples/blob/master/examples/itemviews/simpletreemodel
/simpletreemodel.py
"""

from __future__ import annotations

from collections import OrderedDict
from difflib import SequenceMatcher
import inspect
import logging
from typing import Any

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore
from prettyqt.utils import helpers, treeitem


# TODO: a lot of methods (e.g. rowCount) test if parent.column() > 0. This should probably
# be replaced with an assert.


logger = logging.getLogger(__name__)

MAX_OBJ_STR_LEN = 50


class ObjectBrowserTreeItem(treeitem.TreeItem):
    """Tree node class that can be used to build trees of objects."""

    def __init__(
        self,
        obj,
        name,
        obj_path,
        is_attribute,
        parent: ObjectBrowserTreeItem | None = None,
    ):
        super().__init__(obj, parent=parent)
        # self.parent_item = parent
        # self.obj = obj
        # self.child_items: List[ObjectBrowserTreeItem] = []
        # self.has_children = True
        # self.children_fetched = False
        self.obj_name = str(name)
        self.obj_path = str(obj_path)
        self.is_attribute = is_attribute

    @property
    def is_special_attribute(self) -> bool:
        """Return true if the item represents a dunder attribute."""
        return (
            self.is_attribute
            and self.obj_name.startswith("__")
            and self.obj_name.endswith("__")
        )

    @property
    def is_callable_attribute(self) -> bool:
        """Return true if the items is an attribute and it is callable."""
        return self.is_attribute and callable(self.obj)


class ObjectBrowserTreeModel(custom_models.ColumnItemModel):
    """Model that provides an interface to an objectree that is build of tree items."""

    def __init__(
        self,
        obj: Any,
        obj_name: str = "",
        attr_cols: list[custom_models.ColumnItem] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        """Constructor.

        Args:
            obj (Any): Object to inspect
            obj_name (str, optional): Name of the object
            attr_cols (None, optional): List of Column items
            parent (None, optional): Description
        """
        super().__init__(attr_cols=attr_cols, parent=parent)
        # The root_item is always invisible. If the obj_name is the empty string, the
        # inspectedItem will be the invisible root_item. If the obj_name is given,
        # an invisible root item will be added and the inspectedItem will be its
        # only child. In that case the inspected item will be visible.
        self._inspected_node_is_visible = obj_name != ""

        if self._inspected_node_is_visible:
            self._root_item = ObjectBrowserTreeItem(
                None, "<invisible_root>", "<invisible_root>", None
            )
            self._root_item.children_fetched = True
            self.inspected_item = ObjectBrowserTreeItem(
                obj, obj_name, obj_name, is_attribute=None
            )
            self._root_item.append_child(self.inspected_item)
        else:
            # The root itself will be invisible
            self._root_item = ObjectBrowserTreeItem(
                obj, obj_name, obj_name, is_attribute=None
            )
            self.inspected_item = self._root_item

            # Fetch all items of the root so we can select the first row in the ctor.
            root_index = self.index(0, 0)
            self.fetchMore(root_index)

    def flags(self, index: core.ModelIndex):
        if not index.isValid():
            return constants.NO_CHILDREN
        return constants.IS_ENABLED | constants.IS_SELECTABLE  # type: ignore

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:

        if parent is None:
            logger.debug("parent is None")
            parent = core.ModelIndex()

        parent_item = self.tree_item(parent)

        if not self.hasIndex(row, column, parent):
            logger.debug("hasIndex is False: (%s, %s) %r", row, column, parent_item)
            # logger.warn("Parent index model: {!r} != {!r}".format(parent.model(), self))

            return core.ModelIndex()

        child_item = parent_item.child(row)
        # logger.debug("  {}".format(child_item.obj_path))
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            logger.warn("no child_item")
            return core.ModelIndex()

    def parent(self, index: core.ModelIndex) -> QtCore.QModelIndex:  # type:ignore
        if not index.isValid():
            return core.ModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()  # type: ignore

        if parent_item is None or parent_item == self.root_item:
            return core.ModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent

        if parent.column() > 0:
            # This is taken from the PyQt simpletreemodel example.
            return 0
        else:
            return self.tree_item(parent).child_count()

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return 0
        else:
            return self.tree_item(parent).has_children

    def canFetchMore(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return 0
        else:
            result = not self.tree_item(parent).children_fetched
            # logger.debug("canFetchMore: {} = {}".format(parent, result))
            return result

    def fetchMore(self, parent: core.ModelIndex | None = None):
        """Fetches the children given the model index of a parent node.

        Adds the children to the parent.
        """
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return

        parent_item = self.tree_item(parent)
        if parent_item.children_fetched:
            return

        tree_items = self._fetch_object_children(parent_item.obj, parent_item.obj_path)

        with self.insert_rows(0, len(tree_items) - 1, parent):
            for tree_item in tree_items:
                parent_item.append_child(tree_item)
            parent_item.children_fetched = True

    @property
    def inspected_node_is_visible(self):
        """Return True if the inspected node is visible.

        In that case an invisible root node has been added.
        """
        return self._inspected_node_is_visible

    @property
    def root_item(self) -> ObjectBrowserTreeItem:
        """The root ObjectBrowserTreeItem."""
        return self._root_item

    def root_index(self) -> core.ModelIndex:  # TODO: needed?
        """The index that returns the root element (same as an invalid index)."""
        return core.ModelIndex()

    def inspected_index(self) -> core.ModelIndex:
        """The model index that point to the inspectedItem."""
        if self.inspected_node_is_visible:
            return self.createIndex(0, 0, self.inspected_item)
        else:
            return self.root_index()

    def tree_item(self, index: core.ModelIndex) -> ObjectBrowserTreeItem:
        if not index.isValid():
            return self.root_item
        else:
            return index.internalPointer()  # type: ignore

    def _fetch_object_children(self, obj, obj_path):  # -> List[ObjectBrowserTreeItem]:
        """Fetches the children of a Python object.

        Returns: list of ObjectBrowserTreeItems
        """
        obj_children = []
        path_strings = []

        if isinstance(obj, (list, tuple, set, frozenset)):
            obj_children = [(str(i), j) for i, j in sorted(enumerate(obj))]
            path_strings = [
                f"{obj_path}[{i[0]}]" if obj_path else i[0] for i in obj_children
            ]
        # elif isinstance(obj, (set, frozenset)):
        #     obj_children = [("pop()", elem) for elem in obj]
        #     path_strings = [
        #         "{0}.pop()".format(obj_path) if obj_path else item[0]
        #         for item in obj_children
        #     ]
        elif hasattr(obj, "items") and callable(getattr(obj, "items")):  # dicts etc.
            try:
                obj_children = list(obj.items())
            except Exception as ex:
                # Can happen if the items method expects an argument, for instance the
                # types.DictType.items method expects a dictionary.
                logger.warn("No items expanded. Objects items() call failed: %s", ex)
                obj_children = []

            # Sort keys, except when the object is an OrderedDict.
            if not isinstance(obj, OrderedDict):
                try:
                    obj_children = sorted(obj.items())
                except Exception as ex:
                    logger.debug("Unable to sort dictionary keys: %s", ex)

            path_strings = [
                f"{obj_path}[{item[0]!r}]" if obj_path else item[0]
                for item in obj_children
            ]

        is_attr_list = [False] * len(obj_children)

        # Object attributes
        for attr_name, attr_value in sorted(inspect.getmembers(obj)):
            obj_children.append((attr_name, attr_value))
            path_strings.append(f"{obj_path}.{attr_name}" if obj_path else attr_name)
            is_attr_list.append(True)

        tree_items = []
        for item, path_str, is_attr in zip(obj_children, path_strings, is_attr_list):
            name, child_obj = item
            tree_items.append(ObjectBrowserTreeItem(child_obj, name, path_str, is_attr))

        return tree_items

    def _aux_refresh_tree(self, tree_index: core.ModelIndex):
        """Auxiliary function for refresh_tree that recursively refreshes the tree nodes.

        If the underlying Python object has been changed, we don't want to delete the old
        tree model and create a new one from scratch because this loses all information
        about which nodes are fetched and expanded. Instead the old tree model is updated.
        Using the difflib from the standard library it is determined for a parent node
        which child nodes should be added or removed. This is done based on the node names
        only, not on the node contents (the underlying Python objects). Testing the
        underlying nodes for equality is potentially slow. It is faster to let the
        refreshNode function emit the dataChanged signal for all cells.
        """
        tree_item = self.tree_item(tree_index)
        logger.debug(
            "_aux_refresh_tree(%s): %s%s",
            tree_index,
            tree_item.obj_path,
            "*" if tree_item.children_fetched else "",
        )

        if not tree_item.children_fetched:
            return None

        old_items = tree_item.child_items
        new_items = self._fetch_object_children(tree_item.obj, tree_item.obj_path)

        old_item_names = [(item.obj_name, item.is_attribute) for item in old_items]
        new_item_names = [(item.obj_name, item.is_attribute) for item in new_items]
        seqMatcher = SequenceMatcher(
            isjunk=None, a=old_item_names, b=new_item_names, autojunk=False
        )
        opcodes = seqMatcher.get_opcodes()

        logger.debug("(reversed) opcodes: %s", list(reversed(opcodes)))

        for tag, i1, i2, j1, j2 in reversed(opcodes):

            if 1 or tag != "equal":
                logger.debug(
                    "  {:7s}, a[{}:{}] ({}), b[{}:{}] ({})".format(
                        tag, i1, i2, old_item_names[i1:i2], j1, j2, new_item_names[j1:j2]
                    )
                )

            if tag == "equal":
                # Only when node names are equal is _aux_refresh_tree called recursively.
                assert (
                    i2 - i1 == j2 - j1
                ), f"equal sanity check failed {i2 - i1} != {j2 - j1}"
                for old_row, new_row in zip(range(i1, i2), range(j1, j2)):
                    old_items[old_row].obj = new_items[new_row].obj
                    child_index = self.index(old_row, 0, parent=tree_index)
                    self._aux_refresh_tree(child_index)

            elif tag == "replace":
                # Explicitly remove the old item and insert the new. The old item may have
                # child nodes which indices must be removed by Qt, otherwise it crashes.
                assert (
                    i2 - i1 == j2 - j1
                ), f"replace sanity check failed {i2 - i1} != {j2 - j1}"

                first = i1  # row number of first that will be removed
                last = i1 + i2 - 1  # row number of last element after insertion
                with self.remove_rows(first, last, tree_index):
                    del tree_item.child_items[i1:i2]

                first = i1  # row number of first element after insertion
                last = i1 + j2 - j1 - 1  # row number of last element after insertion
                with self.insert_rows(first, last, tree_index):
                    tree_item.insert_children(i1, new_items[j1:j2])

            elif tag == "delete":
                assert j1 == j2, f"delete sanity check failed. {j1} != {j2}"
                first = i1  # row number of first that will be removed
                last = i1 + i2 - 1  # row number of last element after insertion
                with self.remove_rows(first, last, tree_index):
                    del tree_item.child_items[i1:i2]

            elif tag == "insert":
                assert i1 == i2, f"insert sanity check failed. {i1} != {i2}"
                first = i1
                last = i1 + j2 - j1 - 1
                with self.insert_rows(first, last, tree_index):
                    tree_item.insert_children(i1, new_items[j1:j2])
            else:
                raise ValueError(f"Invalid tag: {tag}")

    def refresh_tree(self):
        """Refreshes the tree model from the underlying root object."""
        logger.info("")
        logger.info("refresh_tree: %s", self.root_item)

        root_item = self.tree_item(self.root_index())
        logger.info("  root_item:      %s (idx=%s)", root_item, self.root_index())
        inspected_item = self.tree_item(self.inspected_index())
        logger.info(
            "  inspected_item: %s (idx=%s)", inspected_item, self.inspected_index()
        )

        assert (
            root_item is inspected_item
        ) != self.inspected_node_is_visible, "sanity check"

        self._aux_refresh_tree(self.inspected_index())

        logger.debug(
            "After _aux_refresh_tree, root_obj: %s",
            helpers.cut_off_str(self.root_item.obj, 80),
        )
        self.root_item.pretty_print()

        # Emit the dataChanged signal for all cells. This is faster than checking which
        # nodes have changed, which may be slow for some underlying Python objects.
        bottom_row = self.rowCount() - 1
        right_column = self.columnCount() - 1
        top_left = self.index(0, 0)
        bottom_right = self.index(bottom_row, right_column)

        logger.debug(f"bottom_right: ({bottom_row}, {right_column})")
        self.dataChanged.emit(top_left, bottom_right)


class ObjectBrowserTreeProxyModel(core.SortFilterProxyModel):
    """Proxy model that overrides the sorting and can filter out items."""

    def __init__(
        self,
        show_callable_attrs: bool = True,
        show_special_attrs: bool = True,
        parent=None,
    ):
        """Constructor.

        :param show_callable_attrs: if True the callables objects,
            i.e. objects (such as function) that  a __call__ method,
            will be displayed (in brown). If False they are hidden.
        :param show_special_attrs: if True the objects special attributes,
            i.e. methods with a name that starts and ends with two underscores,
            will be displayed (in italics). If False they are hidden.
        :param parent: the parent widget
        """
        super().__init__(parent)

        self._show_callables = show_callable_attrs
        self._show_special_attrs = show_special_attrs

    def tree_item(self, proxy_index: core.ModelIndex) -> ObjectBrowserTreeItem:
        index = self.mapToSource(proxy_index)
        return self.sourceModel().tree_item(index)

    def first_item_index(self) -> core.ModelIndex:
        """Return the first child of the root item."""
        # We cannot just call the same function of the source model because the first node
        # there may be hidden.
        source_root_index = self.sourceModel().root_index()
        proxy_root_index = self.mapFromSource(source_root_index)
        first_item_index = self.index(0, 0, proxy_root_index)
        return first_item_index

    def filterAcceptsRow(self, source_row: int, source_parent_index: core.ModelIndex):
        """Return true if the item should be included in the model."""
        parent_item = self.sourceModel().tree_item(source_parent_index)
        tree_item = parent_item.child(source_row)

        accept = (self._show_special_attrs or not tree_item.is_special_attribute) and (
            self._show_callables or not tree_item.is_callable_attribute
        )

        # logger.debug("filterAcceptsRow = {}: {}".format(accept, tree_item))
        return accept

    def get_show_callables(self) -> bool:
        return self._show_callables

    def set_show_callables(self, show_callables: bool):
        """Show/hide show_callables which have a __call__ attribute."""
        logger.debug("set_show_callables: %s", show_callables)
        self._show_callables = show_callables
        self.invalidateFilter()

    def get_show_special_attrs(self) -> bool:
        return self._show_special_attrs

    def set_show_special_attrs(self, show_special_attrs: bool):
        """Show/hide special attributes which begin with an underscore."""
        logger.debug("set_show_special_attrs: %s", show_special_attrs)
        self._show_special_attrs = show_special_attrs
        self.invalidateFilter()
