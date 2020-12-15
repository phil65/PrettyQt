"""Constants module."""
from typing import Literal

from qtpy import QtCore
from bidict import bidict

DISPLAY_ROLE = QtCore.Qt.DisplayRole
USER_ROLE = QtCore.Qt.UserRole
SORT_ROLE = QtCore.Qt.UserRole + 1
NAME_ROLE = QtCore.Qt.UserRole + 2
EDIT_ROLE = QtCore.Qt.EditRole
BACKGROUND_ROLE = QtCore.Qt.BackgroundRole
FOREGROUND_ROLE = QtCore.Qt.ForegroundRole
TOOLTIP_ROLE = QtCore.Qt.ToolTipRole
STATUSTIP_ROLE = QtCore.Qt.StatusTipRole
DECORATION_ROLE = QtCore.Qt.DecorationRole
CHECKSTATE_ROLE = QtCore.Qt.CheckStateRole
ALIGNMENT_ROLE = QtCore.Qt.TextAlignmentRole
FONT_ROLE = QtCore.Qt.FontRole

ALIGN_LEFT = QtCore.Qt.AlignLeft
ALIGN_RIGHT = QtCore.Qt.AlignRight
ALIGN_H_CENTER = QtCore.Qt.AlignHCenter
ALIGN_JUSTIFY = QtCore.Qt.AlignJustify

ALIGN_TOP = QtCore.Qt.AlignTop
ALIGN_BOTTOM = QtCore.Qt.AlignBottom
ALIGN_V_CENTER = QtCore.Qt.AlignVCenter
ALIGN_BASELINE = QtCore.Qt.AlignBaseline

ALIGN_CENTER = QtCore.Qt.AlignCenter
ALIGN_CENTER_LEFT = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft
ALIGN_CENTER_RIGHT = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
ALIGN_TOP_LEFT = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
ALIGN_TOP_RIGHT = QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
ALIGN_TOP_CENTER = QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter
ALIGN_BOTTOM_LEFT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft
ALIGN_BOTTOM_RIGHT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
ALIGN_BOTTOM_CENTER = QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter

HORIZONTAL = QtCore.Qt.Horizontal
VERTICAL = QtCore.Qt.Vertical

ASCENDING = QtCore.Qt.AscendingOrder
DESCENDING = QtCore.Qt.DescendingOrder

DROP_ENABLED = QtCore.Qt.ItemIsDropEnabled
DRAG_ENABLED = QtCore.Qt.ItemIsDragEnabled
IS_ENABLED = QtCore.Qt.ItemIsEnabled
IS_SELECTABLE = QtCore.Qt.ItemIsSelectable
IS_EDITABLE = QtCore.Qt.ItemIsEditable
IS_CHECKABLE = QtCore.Qt.ItemIsUserCheckable
IS_AUTO_TRISTATE = QtCore.Qt.ItemIsAutoTristate
IS_USER_TRISTATE = QtCore.Qt.ItemIsUserTristate
NO_FLAGS = QtCore.Qt.NoItemFlags
NO_CHILDREN = QtCore.Qt.ItemNeverHasChildren

MOVE_ACTION = QtCore.Qt.MoveAction
COPY_ACTION = QtCore.Qt.CopyAction

TEXT_WORD_WRAP = QtCore.Qt.TextWordWrap

CTRL_MOD = QtCore.Qt.ControlModifier

KEY_F11 = QtCore.Qt.Key_F11
KEY_DELETE = QtCore.Qt.Key_Delete


try:
    ALIGNMENTS = bidict(
        left=ALIGN_LEFT,
        right=ALIGN_RIGHT,
        top=ALIGN_TOP,
        bottom=ALIGN_BOTTOM,
        top_left=ALIGN_TOP_LEFT,
        top_right=ALIGN_TOP_RIGHT,
        bottom_left=ALIGN_BOTTOM_LEFT,
        bottom_right=ALIGN_BOTTOM_RIGHT,
        center=ALIGN_CENTER,
    )

    SIDES = bidict(
        left=QtCore.Qt.AlignLeft,
        right=QtCore.Qt.AlignRight,
        top=QtCore.Qt.AlignTop,
        bottom=QtCore.Qt.AlignBottom,
    )
    EDGES = bidict(
        top=QtCore.Qt.TopEdge,
        left=QtCore.Qt.LeftEdge,
        right=QtCore.Qt.RightEdge,
        bottom=QtCore.Qt.BottomEdge,
        top_left=QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge,
        top_right=QtCore.Qt.TopEdge | QtCore.Qt.RightEdge,
        bottom_left=QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge,
        bottom_right=QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge,
    )

    H_ALIGNMENT = bidict(
        left=QtCore.Qt.AlignLeft,
        right=QtCore.Qt.AlignRight,
        center=QtCore.Qt.AlignHCenter,
        justify=QtCore.Qt.AlignJustify,
    )

    V_ALIGNMENT = bidict(
        top=QtCore.Qt.AlignTop,
        bottom=QtCore.Qt.AlignBottom,
        center=QtCore.Qt.AlignVCenter,
        baseline=QtCore.Qt.AlignBaseline,
    )

except TypeError:
    ALIGNMENTS = SIDES = EDGES = H_ALIGNMENT = V_ALIGNMENT = bidict()

EdgeStr = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

AlignmentStr = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

SideStr = Literal["left", "right", "top", "bottom"]

HorizontalAlignmentStr = Literal[
    "left",
    "right",
    "center",
    "justify",
]
VerticalAlignmentStr = Literal[
    "top",
    "bottom",
    "center",
    "baseline",
]

ORIENTATION = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)

OrientationStr = Literal["horizontal", "vertical"]

STATE = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

StateStr = Literal["unchecked", "partial", "checked"]

MATCH_FLAGS = dict(
    exact=QtCore.Qt.MatchExactly,
    contains=QtCore.Qt.MatchContains,
    starts_with=QtCore.Qt.MatchStartsWith,
    ends_with=QtCore.Qt.MatchEndsWith,
    wildcard=QtCore.Qt.MatchWildcard,
    regex=QtCore.Qt.MatchRegExp,
)

MatchFlagStr = Literal[
    "exact", "containts", "starts_with", "ends_with", "wildcard", "regex"
]

FILTER_MODE = bidict(
    starts_with=QtCore.Qt.MatchStartsWith,
    contains=QtCore.Qt.MatchContains,
    ends_with=QtCore.Qt.MatchEndsWith,
)

FilterModeStr = Literal["starts_with", "contains", "ends_with"]
