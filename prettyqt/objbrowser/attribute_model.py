"""Module that defines AttributeModel."""

import logging
import inspect
import pprint
from typing import Callable

from qtpy import QtGui
from prettyqt.utils import columnitem
from prettyqt import gui
from prettyqt.objbrowser import treeitem


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


def get_color(tree_item: treeitem.TreeItem) -> QtGui.QBrush:
    if callable(tree_item.obj):
        return CALLABLE_COLOR
    else:
        return REGULAR_COLOR


def get_font(tree_item: treeitem.TreeItem) -> QtGui.QFont:
    if tree_item.is_special_attribute:
        return SPECIAL_ATTR_FONT
    else:
        return REGULAR_FONT


def get_type(tree_item: treeitem.TreeItem) -> str:
    if inspect.isasyncgen(tree_item.obj):
        return "Async generator"
    if inspect.ismethoddescriptor(tree_item.obj):
        return "Method descriptor"
    if inspect.ismethod(tree_item.obj):
        return "Method"
    elif inspect.isfunction(tree_item.obj):
        return "Function"
    elif inspect.isgeneratorfunction(tree_item.obj):
        return "Generator function"
    elif inspect.isclass(tree_item.obj):
        return "Class"
    elif inspect.ismodule(tree_item.obj):
        return "Module"
    elif inspect.isdatadescriptor(tree_item.obj):
        return "Data descriptor"
    elif inspect.isbuiltin(tree_item.obj):
        return "Builtin"
    return "Attribute"


def safe_tio_call(obj_fn: Callable, tree_item, log_exceptions: bool = False) -> str:
    """Call the obj_fn(tree_item.obj).

    Returns empty string in case of an error.
    """
    tio = tree_item.obj
    try:
        return str(obj_fn(tio))
    except Exception as ex:
        if log_exceptions:
            logger.exception(ex)
        return ""


def safe_data_fn(obj_fn: Callable, log_exceptions: bool = False) -> Callable:
    """Create a function that returns an empty string in case of an exception.

    :param fnobj_fn: function that will be wrapped
    :type obj_fn: object to basestring function
    :returns: function that can be used as AttributeModel data_fn attribute
    :rtype: objbrowser.treeitem.TreeItem to string function
    """

    def data_fn(tree_item: treeitem.TreeItem):
        """Call the obj_fn(tree_item.obj).

        Returns empty string in case of an error
        """
        return safe_tio_call(obj_fn, tree_item, log_exceptions=log_exceptions)

    return data_fn


def tio_predicates(tree_item: treeitem.TreeItem) -> str:
    """Return the inspect module predicates that are true for this object."""
    predicates = [pred.__name__ for pred in _ALL_PREDICATES if pred(tree_item.obj)]
    return ", ".join(predicates)


def tio_is_attribute(tree_item: treeitem.TreeItem) -> str:
    """Return 'True' if the tree item object is an attribute of the parent."""
    if tree_item.is_attribute is None:
        return ""
    else:
        return str(tree_item.is_attribute)


def tio_doc_str(tree_item: treeitem.TreeItem) -> str:
    """Return the doc string of an object."""
    try:
        return tree_item.obj.__doc__
    except AttributeError:
        return "<no doc string found>"


#######################
# Column definitions ##
#######################

ATTR_MODEL_NAME = columnitem.ColumnItem(
    name="Name",
    doc="The name of the object.",
    label=lambda tree_item: tree_item.obj_name if tree_item.obj_name else "<root>",
    col_visible=True,
    width=columnitem.SMALL_COL_WIDTH,
    font=get_font,
    foreground_color=get_color,
)

ATTR_MODEL_DESCRIPTION = columnitem.ColumnItem(
    name="Description",
    doc="Description of the object.",
    label=lambda tree_item: get_type(tree_item),
    col_visible=True,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_PATH = columnitem.ColumnItem(
    name="Path",
    doc="A path to the data: e.g. var[1]['a'].item",
    label=lambda tree_item: tree_item.obj_path if tree_item.obj_path else "<root>",
    col_visible=True,
    width=columnitem.MEDIUM_COL_WIDTH,
)


ATTR_MODEL_STR = columnitem.ColumnItem(
    name="str",
    doc="""The string representation of the object using the str() function.""",
    label=lambda tree_item: str(tree_item.obj),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
    line_wrap="boundary_or_anywhere",
)

ATTR_MODEL_REPR = columnitem.ColumnItem(
    name="repr",
    doc="The string representation of the object using the repr() function.",
    label=lambda tree_item: repr(tree_item.obj),
    col_visible=True,
    width=columnitem.MEDIUM_COL_WIDTH,
    line_wrap="boundary_or_anywhere",
)

ATTR_MODEL_TYPE = columnitem.ColumnItem(
    name="Type",
    doc="Type of the object determined using the builtin type() function",
    label=lambda tree_item: str(type(tree_item.obj)),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_CLASS = columnitem.ColumnItem(
    name="Type name",
    doc="The name of the class of the object via obj.__class__.__name__",
    label=lambda tree_item: type(tree_item.obj).__name__,
    col_visible=True,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_LENGTH = columnitem.ColumnItem(
    name="Length",
    doc="The length of the object using the len() function",
    # data_fn     = tio_length,
    label=safe_data_fn(len),
    col_visible=False,
    alignment=columnitem.ALIGN_RIGHT,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_ID = columnitem.ColumnItem(
    name="id",
    doc="The identifier of the object with calculated using the id() function",
    label=lambda tree_item: "0x{:X}".format(id(tree_item.obj)),
    col_visible=False,
    alignment=columnitem.ALIGN_RIGHT,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_IS_ATTRIBUTE = columnitem.ColumnItem(
    name="Attribute",
    doc="""The object is an attribute of the parent (opposed to e.g. a list element).
                     Attributes are displayed in italics in the table.
                  """,
    label=tio_is_attribute,
    col_visible=False,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_CALLABLE = columnitem.ColumnItem(
    name="Callable",
    doc="""True if the object is callable.
                     Determined with the `callable` built-in function.
                     Callable objects are displayed in blue in the table.
                  """,
    label=None,
    checkstate=lambda tree_item: callable(tree_item.obj),
    col_visible=True,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_IS_ROUTINE = columnitem.ColumnItem(
    name="Routine",
    doc="""True if the object is a user-defined or built-in function or method.
                     Determined with the inspect.isroutine() method.
                  """,
    label=None,
    checkstate=lambda tree_item: inspect.isroutine(tree_item.obj),
    col_visible=False,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_IS_BUILTIN = columnitem.ColumnItem(
    name="Builtin",
    doc="""True if the object is a builtin.
                     Determined with the inspect.isbuiltin() method.
                  """,
    label=None,
    checkstate=lambda tree_item: inspect.isbuiltin(tree_item.obj),
    col_visible=False,
    width=columnitem.SMALL_COL_WIDTH,
)

ATTR_MODEL_PRED = columnitem.ColumnItem(
    name="Inspect predicates",
    doc="Predicates from the inspect module",
    label=tio_predicates,
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_PRETTY_PRINT = columnitem.ColumnItem(
    name="Pretty print",
    doc="Pretty printed representation of the object using the pprint module.",
    label=lambda tree_item: _PRETTY_PRINTER.pformat(tree_item.obj),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)


ATTR_MODEL_GET_DOC = columnitem.ColumnItem(
    name="inspect.getdoc",
    doc="The object's doc string, leaned up by inspect.getdoc()",
    label=safe_data_fn(inspect.getdoc),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_GET_COMMENTS = columnitem.ColumnItem(
    name="inspect.getcomments",
    doc="Comments above the object's definition. Retrieved using inspect.getcomments()",
    label=lambda tree_item: inspect.getcomments(tree_item.obj),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_GET_MODULE = columnitem.ColumnItem(
    name="inspect.getmodule",
    doc="The object's module. Retrieved using inspect.module",
    label=safe_data_fn(inspect.getmodule),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_GET_FILE = columnitem.ColumnItem(
    name="inspect.getfile",
    doc="The object's file. Retrieved using inspect.getfile",
    label=safe_data_fn(inspect.getfile),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)

ATTR_MODEL_GET_SOURCE_FILE = columnitem.ColumnItem(
    name="inspect.getsourcefile",  # calls inspect.getfile()
    doc="The object's file. Retrieved using inspect.getsourcefile",
    label=safe_data_fn(inspect.getsourcefile),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
)


ATTR_MODEL_GET_SOURCE = columnitem.ColumnItem(
    name="Inspect.getsource",
    doc="The source code of an object retrieved using inspect.getsource",
    label=safe_data_fn(inspect.getsource),
    col_visible=False,
    width=columnitem.MEDIUM_COL_WIDTH,
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
