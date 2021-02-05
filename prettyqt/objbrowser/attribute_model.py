"""Module that defines AttributeModel."""

from __future__ import annotations

import inspect
import logging
import pprint
from typing import Callable

from prettyqt import constants, custom_models, gui
from prettyqt.qt import QtGui
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

CALLABLE_COLOR = QtGui.QBrush(gui.Color("mediumblue"))
REGULAR_COLOR = QtGui.QBrush(gui.Color("black"))

REGULAR_FONT = QtGui.QFont()  # Font for members (non-functions)
SPECIAL_ATTR_FONT = QtGui.QFont()  # Font for __special_attributes__
SPECIAL_ATTR_FONT.setItalic(True)


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


def get_type(tree_item: treeitem.TreeItem) -> str:

    for k, v in TYPE_CHECK.items():
        if k(tree_item.obj):
            return v
    return "Attribute"


def safe_data_fn(
    obj_fn: Callable,
    log_exceptions: bool = False,
) -> Callable:
    """Create a function that returns an empty string in case of an exception.

    :param fnobj_fn: function that will be wrapped
    :type obj_fn: object to basestring function
    :returns: function that can be used as AttributeModel data_fn attribute
    :rtype: custom_models.treeitem.TreeItem to string function
    """

    def data_fn(tree_item: treeitem.TreeItem) -> str:
        """Call the obj_fn(tree_item.obj).

        Returns empty string in case of an error
        """
        try:
            return str(obj_fn(tree_item.obj))
        except Exception as ex:
            if log_exceptions:
                logger.exception(ex)
            return ""

    return data_fn


#######################
# Column definitions ##
#######################

ATTR_MODEL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="The name of the object.",
    label=lambda tree_item: tree_item.obj_name if tree_item.obj_name else "<root>",
    col_visible=True,
    width="small",
    font=lambda x: SPECIAL_ATTR_FONT if x.is_special_attribute else REGULAR_FONT,
    foreground_color=lambda x: CALLABLE_COLOR if callable(x.obj) else REGULAR_COLOR,
)

ATTR_MODEL_DESCRIPTION = custom_models.ColumnItem(
    name="Description",
    doc="Description of the object.",
    label=lambda tree_item: get_type(tree_item),
    col_visible=True,
    width="small",
)

ATTR_MODEL_PATH = custom_models.ColumnItem(
    name="Path",
    doc="A path to the data: e.g. var[1]['a'].item",
    label=lambda tree_item: tree_item.obj_path if tree_item.obj_path else "<root>",
    col_visible=True,
    width="medium",
)


ATTR_MODEL_STR = custom_models.ColumnItem(
    name="str",
    doc="""The string representation of the object using the str() function.""",
    label=lambda tree_item: str(tree_item.obj),
    col_visible=False,
    width="medium",
    line_wrap="boundary_or_anywhere",
)

ATTR_MODEL_REPR = custom_models.ColumnItem(
    name="repr",
    doc="The string representation of the object using the repr() function.",
    label=lambda tree_item: repr(tree_item.obj),
    col_visible=True,
    width="medium",
    line_wrap="boundary_or_anywhere",
)

ATTR_MODEL_TYPE = custom_models.ColumnItem(
    name="Type",
    doc="Type of the object determined using the builtin type() function",
    label=lambda tree_item: str(type(tree_item.obj)),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_CLASS = custom_models.ColumnItem(
    name="Type name",
    doc="The name of the class of the object via obj.__class__.__name__",
    label=lambda tree_item: type(tree_item.obj).__name__,
    col_visible=True,
    width="medium",
)

ATTR_MODEL_LENGTH = custom_models.ColumnItem(
    name="Length",
    doc="The length of the object using the len() function",
    # data_fn     = tio_length,
    label=safe_data_fn(len),
    col_visible=False,
    alignment=constants.ALIGN_RIGHT,  # type: ignore
    width="small",
)

ATTR_MODEL_ID = custom_models.ColumnItem(
    name="id",
    doc="The identifier of the object with calculated using the id() function",
    label=lambda tree_item: f"0x{id(tree_item.obj):X}",
    col_visible=False,
    alignment=constants.ALIGN_RIGHT,  # type: ignore
    width="small",
)

ATTR_MODEL_IS_ATTRIBUTE = custom_models.ColumnItem(
    name="Attribute",
    doc="""The object is an attribute of the parent (opposed to e.g. a list element).
                     Attributes are displayed in italics in the table.
                  """,
    label=lambda x: "" if x.is_attribute is None else str(x.is_attribute),
    col_visible=False,
    width="small",
)

ATTR_MODEL_CALLABLE = custom_models.ColumnItem(
    name="Callable",
    doc="""True if the object is callable.
                     Determined with the `callable` built-in function.
                     Callable objects are displayed in blue in the table.
                  """,
    label=None,
    checkstate=lambda tree_item: callable(tree_item.obj),
    col_visible=True,
    width="small",
)

ATTR_MODEL_IS_ROUTINE = custom_models.ColumnItem(
    name="Routine",
    doc="""True if the object is a user-defined or built-in function or method.
                     Determined with the inspect.isroutine() method.
                  """,
    label=None,
    checkstate=lambda tree_item: inspect.isroutine(tree_item.obj),
    col_visible=False,
    width="small",
)

ATTR_MODEL_IS_BUILTIN = custom_models.ColumnItem(
    name="Builtin",
    doc="""True if the object is a builtin.
                     Determined with the inspect.isbuiltin() method.
                  """,
    label=None,
    checkstate=lambda tree_item: inspect.isbuiltin(tree_item.obj),
    col_visible=False,
    width="small",
)

ATTR_MODEL_PRED = custom_models.ColumnItem(
    name="Inspect predicates",
    doc="Predicates from the inspect module",
    label=lambda x: ", ".join(pred.__name__ for pred in _ALL_PREDICATES if pred(x.obj)),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_PRETTY_PRINT = custom_models.ColumnItem(
    name="Pretty print",
    doc="Pretty printed representation of the object using the pprint module.",
    label=lambda tree_item: _PRETTY_PRINTER.pformat(tree_item.obj),
    col_visible=False,
    width="medium",
)


ATTR_MODEL_GET_DOC = custom_models.ColumnItem(
    name="inspect.getdoc",
    doc="The object's doc string, leaned up by inspect.getdoc()",
    label=safe_data_fn(inspect.getdoc),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_GET_COMMENTS = custom_models.ColumnItem(
    name="inspect.getcomments",
    doc="Comments above the object's definition. Retrieved using inspect.getcomments()",
    label=lambda tree_item: inspect.getcomments(tree_item.obj),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_GET_MODULE = custom_models.ColumnItem(
    name="inspect.getmodule",
    doc="The object's module. Retrieved using inspect.module",
    label=safe_data_fn(inspect.getmodule),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_GET_FILE = custom_models.ColumnItem(
    name="inspect.getfile",
    doc="The object's file. Retrieved using inspect.getfile",
    label=safe_data_fn(inspect.getfile),
    col_visible=False,
    width="medium",
)

ATTR_MODEL_GET_SOURCE_FILE = custom_models.ColumnItem(
    name="inspect.getsourcefile",  # calls inspect.getfile()
    doc="The object's file. Retrieved using inspect.getsourcefile",
    label=safe_data_fn(inspect.getsourcefile),
    col_visible=False,
    width="medium",
)


ATTR_MODEL_GET_SOURCE = custom_models.ColumnItem(
    name="Inspect.getsource",
    doc="The source code of an object retrieved using inspect.getsource",
    label=safe_data_fn(inspect.getsource),
    col_visible=False,
    width="medium",
)


DEFAULT_ATTR_COLS = [
    ATTR_MODEL_NAME,
    ATTR_MODEL_DESCRIPTION,
    ATTR_MODEL_PATH,
    ATTR_MODEL_STR,
    ATTR_MODEL_REPR,
    ATTR_MODEL_LENGTH,
    ATTR_MODEL_TYPE,
    ATTR_MODEL_CLASS,
    ATTR_MODEL_ID,
    ATTR_MODEL_IS_ATTRIBUTE,
    ATTR_MODEL_CALLABLE,
    ATTR_MODEL_IS_ROUTINE,
    ATTR_MODEL_IS_BUILTIN,
    ATTR_MODEL_PRED,
    ATTR_MODEL_GET_MODULE,
    ATTR_MODEL_GET_FILE,
    ATTR_MODEL_GET_SOURCE_FILE,
]

DEFAULT_ATTR_DETAILS = [
    ATTR_MODEL_PATH,  # to allow for copy/paste
    ATTR_MODEL_STR,  # Too similar to unicode column
    ATTR_MODEL_REPR,
    ATTR_MODEL_PRETTY_PRINT,
    ATTR_MODEL_GET_DOC,
    ATTR_MODEL_GET_COMMENTS,
    # ATTR_MODEL_GET_MODULE, # not used, already in table
    ATTR_MODEL_GET_FILE,
    # ATTR_MODEL_GET_SOURCE_FILE,  # not used, already in table
    ATTR_MODEL_GET_SOURCE,
]

# Sanity check for duplicates
assert len(DEFAULT_ATTR_COLS) == len(set(DEFAULT_ATTR_COLS))
assert len(DEFAULT_ATTR_DETAILS) == len(set(DEFAULT_ATTR_DETAILS))
