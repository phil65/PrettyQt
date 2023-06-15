from __future__ import annotations

from collections.abc import Iterable, Mapping
from difflib import SequenceMatcher
import inspect
import logging

from prettyqt import constants, core, custom_models
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)


class ObjectBrowserTreeItem(treeitem.TreeItem):
    """Tree node class that can be used to build trees of objects."""

    __slots__ = ("obj_name", "obj_path", "is_attribute")

    def __init__(
        self,
        obj,
        name: str = "",
        obj_path="",
        is_attribute: bool = False,
        parent: ObjectBrowserTreeItem | None = None,
    ):
        super().__init__(obj, parent=parent)
        self.obj_name = name
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


class ObjectBrowserTreeModel(custom_models.ColumnItemModel):
    TreeItem = ObjectBrowserTreeItem

    @classmethod
    def supports(cls, typ):
        return True

    def get_path_for_index(self, index: core.ModelIndex) -> str:
        """Get the path for the object referenced by index.

        Example: An.example = {"a": [b, c, {"d": e}]}
                 -> path of e: An.example["a"][2]["d"]
        """
        # TODO: not used yet, better rework ColumnItemModel first
        treeitem = index.data(constants.USER_ROLE)
        prev_data = treeitem.obj
        pieces = []
        while (index := index.parent()).isValid():
            treeitem = index.data(constants.USER_ROLE)
            data = treeitem.obj
            match data:
                case Mapping():
                    for k, v in data.items():
                        if v is prev_data:
                            pieces.append(f"[{k!r}]")
                            break
                case Iterable():
                    pieces.append(f"[{data.index(prev_data)}]")
                case _:
                    # or should this be treeitem.obj_name?
                    pieces.append(f".{prev_data.__name__}")
            prev_data = data
        pieces.append(treeitem.obj_name)
        return "".join(reversed(pieces))

    def _fetch_object_children(
        self, treeitem: treeitem.TreeItem
    ) -> list[ObjectBrowserTreeItem]:
        """Fetch the children of a Python object.

        Returns: list of ObjectBrowserTreeItems
        """
        obj_children = []
        path_strings = []
        obj = treeitem.obj
        obj_path = treeitem.obj_path
        if isinstance(obj, list | tuple | set | frozenset):
            obj_children = [(str(i), j) for i, j in sorted(enumerate(obj))]
            path_strings = [
                f"{obj_path}[{i[0]}]" if obj_path else i[0] for i in obj_children
            ]
        elif isinstance(obj, Mapping):
            obj_children = list(obj.items())
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

        return [
            ObjectBrowserTreeItem(obj=val, name=name, obj_path=p, is_attribute=is_attr)
            for (name, val), p, is_attr in zip(obj_children, path_strings, is_attr_list)
        ]

    def _aux_refresh_tree(self, tree_index: core.ModelIndex):
        """Refresh the tree nodes recursively, auxiliary.

        If the underlying Python object has been changed, we don't want to delete the old
        tree model and create a new one from scratch because this loses all information
        about which nodes are fetched and expanded. Instead the old tree model is updated.
        Using the difflib from the standard library it is determined for a parent node
        which child nodes should be added or removed. This is done based on the node names
        only, not on the node contents (the underlying Python objects). Testing the
        underlying nodes for equality is potentially slow. It is faster to let the
        refreshNode function emit the dataChanged signal for all cells.
        """
        tree_item = self.data_by_index(tree_index)
        if not tree_item.children_fetched:
            return None
        old_items = tree_item.child_items
        new_items = self._fetch_object_children(tree_item)

        old_item_names = [(item.obj_name, item.is_attribute) for item in old_items]
        new_item_names = [(item.obj_name, item.is_attribute) for item in new_items]
        seq_matcher = SequenceMatcher(
            isjunk=None, a=old_item_names, b=new_item_names, autojunk=False
        )
        opcodes = seq_matcher.get_opcodes()

        logger.debug("(reversed) opcodes: %s", list(reversed(opcodes)))

        for tag, i1, i2, j1, j2 in reversed(opcodes):
            match tag:
                case "equal":
                    # when node names are equal is aux_refresh_tree called recursively.
                    for old_row, new_row in zip(range(i1, i2), range(j1, j2)):
                        old_items[old_row].obj = new_items[new_row].obj
                        child_index = self.index(old_row, 0, parent=tree_index)
                        self._aux_refresh_tree(child_index)

                case "replace":
                    # Remove the old item and insert the new. The old item may have child
                    # nodes which indices must be removed by Qt, otherwise it crashes.
                    first = i1  # row number of first that will be removed
                    last = i1 + i2 - 1  # row number of last element after insertion
                    with self.remove_rows(first, last, tree_index):
                        del tree_item.child_items[i1:i2]

                    first = i1  # row number of first element after insertion
                    last = i1 + j2 - j1 - 1  # row number of last element after insertion
                    with self.insert_rows(first, last, tree_index):
                        tree_item.insert_children(i1, new_items[j1:j2])

                case "delete":
                    first = i1  # row number of first that will be removed
                    last = i1 + i2 - 1  # row number of last element after insertion
                    with self.remove_rows(first, last, tree_index):
                        del tree_item.child_items[i1:i2]

                case "insert":
                    first = i1
                    last = i1 + j2 - j1 - 1
                    with self.insert_rows(first, last, tree_index):
                        tree_item.insert_children(i1, new_items[j1:j2])
                case _:
                    raise ValueError(f"Invalid tag: {tag}")

    def refresh_tree(self):
        if self._show_root:
            index = self.createIndex(0, 0, self.inspected_item)
        else:
            index = self.root_index()
        """Refresh the tree model from the underlying root object."""
        self._aux_refresh_tree(index)
        # Emit the dataChanged signal for all cells. This is faster than checking which
        # nodes have changed, which may be slow for some underlying Python objects.
        self.update_all()


class ObjectBrowserTreeProxyModel(core.SortFilterProxyModel):
    """Proxy model that overrides the sorting and can filter out items."""

    def __init__(
        self, show_callable_attrs: bool = True, show_special_attrs: bool = True, **kwargs
    ):
        super().__init__(**kwargs)

        self._show_callables = show_callable_attrs
        self._show_special_attrs = show_special_attrs

    def data_by_index(self, proxy_index: core.ModelIndex) -> ObjectBrowserTreeItem:
        index = self.mapToSource(proxy_index)
        return self.get_source_model().data_by_index(index)

    def filterAcceptsRow(self, source_row: int, source_parent_index: core.ModelIndex):
        """Return true if the item should be included in the model."""
        parent_item = self.get_source_model().data_by_index(source_parent_index)
        tree_item = parent_item.child(source_row)
        is_callable_attr = tree_item.is_attribute and callable(tree_item.obj)
        return (self._show_special_attrs or not tree_item.is_special_attribute) and (
            self._show_callables or not is_callable_attr
        )

    def get_show_callables(self) -> bool:
        return self._show_callables

    def set_show_callables(self, show_callables: bool):
        """Show/hide show_callables which have a __call__ attribute."""
        self._show_callables = show_callables
        self.invalidateRowsFilter()

    def get_show_special_attrs(self) -> bool:
        return self._show_special_attrs

    def set_show_special_attrs(self, show_special_attrs: bool):
        """Show/hide special attributes which begin with an underscore."""
        self._show_special_attrs = show_special_attrs
        self.invalidateRowsFilter()


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.objbrowser.attribute_model import DEFAULT_ATTR_COLS

    app = widgets.app()
    with app.debug_mode():
        obj = dict(a=[0, 1, 2, 3, dict(b=5)], b={"test": {"test2": 5}})
        model = ObjectBrowserTreeModel(obj, columns=DEFAULT_ATTR_COLS, show_root=False)
        obj_tree = widgets.TreeView()
        obj_tree.setRootIsDecorated(True)
        obj_tree.setAlternatingRowColors(True)
        obj_tree.set_model(model)
        obj_tree.selectionModel().currentChanged.connect(model.get_path_for_index)
        obj_tree.set_selection_behavior("rows")
        obj_tree.setUniformRowHeights(True)
        obj_tree.setAnimated(True)
        obj_tree.show()
        app.main_loop()
