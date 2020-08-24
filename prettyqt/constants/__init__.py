# -*- coding: utf-8 -*-

"""Constants module."""

from qtpy import QtCore

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
ALIGN_TOP_LEFT = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
ALIGN_TOP_RIGHT = QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
ALIGN_BOTTOM_LEFT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft
ALIGN_BOTTOM_RIGHT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight

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
NO_FLAGS = QtCore.Qt.NoItemFlags
NO_CHILDREN = QtCore.Qt.NoItemFlags

MOVE_ACTION = QtCore.Qt.MoveAction
COPY_ACTION = QtCore.Qt.CopyAction

TEXT_WORD_WRAP = QtCore.Qt.TextWordWrap

CTRL_MOD = QtCore.Qt.ControlModifier

KEY_F11 = QtCore.Qt.Key_F11
KEY_DELETE = QtCore.Qt.Key_Delete
