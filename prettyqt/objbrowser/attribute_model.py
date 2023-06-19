"""Module that defines AttributeModel."""

from __future__ import annotations

from collections.abc import Callable
import contextlib
import inspect
import logging
import pprint

from prettyqt import constants, custom_models, gui


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
                return gui.QColor("mediumblue") if callable(item.obj) else None
            case constants.FONT_ROLE:
                font = gui.QFont()
                font.setItalic(True)
                return font if item.is_special_attribute else None


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
                    return len(item)


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
                return bool(item.is_attribute)


class IsCallableColumn(custom_models.ColumnItem):
    name = "Is callable"
    doc = "Whether the object is an callable (like functions or classes)."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return callable(item)


class IsRoutineColumn(custom_models.ColumnItem):
    name = "Is routine"
    doc = "True if the object is a user-defined or built-in function or method."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return inspect.isroutine(item)


class IsBuiltinColumn(custom_models.ColumnItem):
    name = "Builtin"
    doc = "True if the object is a user-defined or built-in function or method."

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.CHECKSTATE_ROLE:
                return inspect.isbuiltin(item)


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
    doc = ("Pretty printed representation of the object using the pprint module.",)

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
    doc = ("Comments above the object's definition.",)

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                return inspect.getcomments(item)


class ModuleColumn(custom_models.ColumnItem):
    name = "Module"
    doc = ("Module of given object.",)

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getmodule(item)


class FileColumn(custom_models.ColumnItem):
    name = "File"
    doc = ("File of the given object.",)

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getfile(item)


class SourceFileColumn(custom_models.ColumnItem):
    name = "SourceFile"
    doc = ("Source file of given object.",)

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getsourcefile(item)


class SourceCodeColumn(custom_models.ColumnItem):
    name = "SourceCode"
    doc = ("Source code of given object.",)

    def get_data(self, item, role: constants.ItemDataRole = constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE:
                with contextlib.suppress(Exception):
                    return inspect.getsource(item)


DEFAULT_ATTR_COLS = [
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
    FileColumn,
    SourceFileColumn,
]
