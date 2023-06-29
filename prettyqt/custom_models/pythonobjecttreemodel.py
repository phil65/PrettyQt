from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
import contextlib

from difflib import SequenceMatcher
import inspect
import logging
import pprint

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)


_PRETTY_PRINTER = pprint.PrettyPrinter(indent=4)

_ALL_PREDICATES = (
    inspect.isgenerator,
    inspect.istraceback,
    inspect.isframe,
    inspect.iscode,
    inspect.isabstract,
    inspect.isgetsetdescriptor,
    inspect.ismemberdescriptor,
)


TYPE_CHECK: dict[Callable, str] = {
    inspect.isasyncgen: "Async generator",
    inspect.ismethoddescriptor: "Method descriptor",
    inspect.ismethod: "Method",
    inspect.isfunction: "Function",
    inspect.isgeneratorfunction: "Generator function",
    inspect.isclass: "Class",
    inspect.ismodule: "Module",
    inspect.isdatadescriptor: "Data descriptor",
    inspect.isbuiltin: "Builtin",
}


class NameColumn(custom_models.ColumnItem):
    name = "Name"
    doc = "The name of the object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj_name or "<root>"
            case constants.FOREGROUND_ROLE:
                return gui.QColor("green") if callable(item.obj) else None
            case constants.FONT_ROLE:
                if (
                    item.is_attribute
                    and item.obj_name.startswith("__")
                    and item.obj_name.endswith("__")
                ):
                    font = gui.QFont()
                    font.setItalic(True)
                    return font
            case constants.USER_ROLE:
                return item


class DescriptionColumn(custom_models.ColumnItem):
    name = "Description"
    doc = "Description of the object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return next(
                    (v for k, v in TYPE_CHECK.items() if k(item.obj)), "Attribute"
                )


class PathColumn(custom_models.ColumnItem):
    name = "Path"
    doc = "A path to the data: e.g. var[1]['a'].item"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj_path or "<root>"


class StrColumn(custom_models.ColumnItem):
    name = "Str"
    doc = "The string representation of the object using the str() function."
    # line_wrap = "boundary_or_anywhere"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return str(item.obj)


class ReprColumn(custom_models.ColumnItem):
    name = "Repr"
    doc = "The string representation of the object using the repr() function."
    # line_wrap = "boundary_or_anywhere"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return repr(item.obj)


class TypeColumn(custom_models.ColumnItem):
    name = "Type"
    doc = "Type of the object determined using the builtin type() function."
    # line_wrap = "boundary_or_anywhere"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return str(type(item.obj))


class ClassColumn(custom_models.ColumnItem):
    name = "Class"
    doc = "Class name of the object."
    # line_wrap = "boundary_or_anywhere"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return type(item.obj).__name__


class LengthColumn(custom_models.ColumnItem):
    name = "Length"
    doc = "Length of the object if available."
    # line_wrap = "boundary_or_anywhere"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return str(len(item))


class IdColumn(custom_models.ColumnItem):
    name = "Id"
    doc = "The identifier of the object calculated using the id() function."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return f"0x{id(item.obj):X}"


class AttributeColumn(custom_models.ColumnItem):
    name = "Attribute"
    doc = "Whether the object is an attribute."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(bool(item.is_attribute))


class IsCallableColumn(custom_models.ColumnItem):
    name = "Is callable"
    doc = "Whether the object is an callable (like functions or classes)."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(callable(item))


class IsRoutineColumn(custom_models.ColumnItem):
    name = "Is routine"
    doc = "True if the object is a user-defined or built-in function or method."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(inspect.isroutine(item))


class IsBuiltinColumn(custom_models.ColumnItem):
    name = "Builtin"
    doc = "True if the object is a user-defined or built-in function or method."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(inspect.isbuiltin(item))


class PredicateColumn(custom_models.ColumnItem):
    name = "Predicate"

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return ", ".join(
                    pred.__name__ for pred in _ALL_PREDICATES if pred(item.obj)
                )


class PrettyPrintColumn(custom_models.ColumnItem):
    name = "Pretty print"
    doc = "Pretty printed representation of the object using the pprint module."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return _PRETTY_PRINTER.pformat(item.obj)


class DocStringColumn(custom_models.ColumnItem):
    name = "Docstring"
    doc = "Docstring from source code."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getdoc(item)


class CommentsColumn(custom_models.ColumnItem):
    name = "Comments"
    doc = "Comments above the object's definition."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return inspect.getcomments(item)


class ModuleColumn(custom_models.ColumnItem):
    name = "Module"
    doc = "Module of given object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getmodule(item)


class FileColumn(custom_models.ColumnItem):
    name = "File"
    doc = "File of the given object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getfile(item)


class SourceFileColumn(custom_models.ColumnItem):
    name = "SourceFile"
    doc = "Source file of given object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getsourcefile(item)


class SourceCodeColumn(custom_models.ColumnItem):
    name = "SourceCode"
    doc = "Source code of given object."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getsource(item)


class PythonObjectTreeItem(treeitem.TreeItem):
    """Tree node class that can be used to build trees of objects."""

    __slots__ = ("obj_name", "obj_path", "is_attribute")

    def __init__(
        self,
        obj,
        name: str = "",
        obj_path="",
        is_attribute: bool = False,
        parent: PythonObjectTreeItem | None = None,
    ):
        super().__init__(obj, parent=parent)
        self.obj_name = name
        self.obj_path = str(obj_path)
        self.is_attribute = is_attribute


class PythonObjectTreeModel(custom_models.ColumnItemModel):
    TreeItem = PythonObjectTreeItem

    COLUMNS = [
        NameColumn,
        DescriptionColumn,
        PathColumn,
        StrColumn,
        ReprColumn,
        LengthColumn,
        TypeColumn,
        ClassColumn,
        IdColumn,
        AttributeColumn,
        IsCallableColumn,
        IsRoutineColumn,
        IsBuiltinColumn,
        PredicateColumn,
        ModuleColumn,
        # FileColumn,
        # SourceFileColumn,
    ]

    def __init__(self, obj, parent=None):
        super().__init__(obj, self.COLUMNS, show_root=False, parent=parent)

    @classmethod
    def supports(cls, instance) -> bool:
        return True

    def get_path_for_index(self, index: core.ModelIndex) -> str:
        """Get the path for the object referenced by index.

        Example: An.example = {"a": [b, c, {"d": e}]}
                 -> path of e: An.example["a"][2]["d"]
        """
        # TODO: not used yet, better rework ColumnItemModel first
        treeitem = index.data(constants.USER_ROLE)
        if treeitem is None:
            return
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
        logger.info(pieces)
        return "".join(reversed(pieces))

    def _fetch_object_children(
        self, treeitem: treeitem.TreeItem
    ) -> list[PythonObjectTreeItem]:
        """Fetch the children of a Python object.

        Returns: list of PythonObjectTreeItems
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
            PythonObjectTreeItem(obj=val, name=name, obj_path=p, is_attribute=is_attr)
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


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        obj = dict(a=[0, 1, 2, 3, dict(b=5)], b={"test": {"test2": 5}})
        model = PythonObjectTreeModel(obj)
        obj_tree = widgets.TreeView()
        obj_tree.setRootIsDecorated(True)
        obj_tree.setAlternatingRowColors(True)
        obj_tree.set_model(model)
        obj_tree.selectionModel().currentRowChanged.connect(model.get_path_for_index)
        obj_tree.set_selection_behavior("rows")
        obj_tree.setUniformRowHeights(True)
        obj_tree.show()
        app.exec()
