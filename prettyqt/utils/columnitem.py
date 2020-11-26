# -*- coding: utf-8 -*-

from typing import Callable, Optional, Union
from dataclasses import dataclass

from prettyqt import constants
from prettyqt.utils import bidict

from qtpy import QtGui

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200

ALIGNMENTS = bidict(
    left=constants.ALIGN_LEFT,
    right=constants.ALIGN_RIGHT,
    top=constants.ALIGN_TOP,
    bottom=constants.ALIGN_BOTTOM,
    top_left=constants.ALIGN_TOP_LEFT,
    top_right=constants.ALIGN_TOP_RIGHT,
    bottom_left=constants.ALIGN_BOTTOM_LEFT,
    bottom_right=constants.ALIGN_BOTTOM_RIGHT,
    center=constants.ALIGN_CENTER,
)


@dataclass(frozen=True)
class ColumnItem:
    """Determines how an object attribute is shown."""

    name: str
    label: Optional[Callable]
    checkstate: Optional[Callable] = None
    doc: str = "<no help available>"
    col_visible: bool = True
    width: int = SMALL_COL_WIDTH
    alignment: Optional[Union[Callable, int]] = None
    line_wrap: str = "none"
    foreground_color: Optional[Union[Callable, str]] = None
    background_color: Optional[Union[Callable, str]] = None
    decoration: Optional[Union[Callable, QtGui.QIcon]] = None
    font: Optional[Union[Callable, QtGui.QFont]] = None
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False

    def get_name(self):
        return self.name

    def get_flag(self):
        flag = constants.NO_FLAGS
        if self.selectable:
            flag |= constants.IS_SELECTABLE
        if self.enabled:
            flag |= constants.IS_ENABLED
        if self.editable:
            flag |= constants.IS_EDITABLE
        if self.checkable:
            flag |= constants.IS_CHECKABLE
        if self.tristate:
            flag |= constants.IS_USER_TRISTATE
        return flag

    def get_label(self, tree_item):
        if self.label is None:
            return ""
        elif callable(self.label):
            return self.label(tree_item)
        return self.label

    def get_checkstate(self, tree_item):
        if self.checkstate is None:
            return None
        elif callable(self.checkstate):
            return self.checkstate(tree_item)
        return self.checkstate

    def get_font(self, tree_item):
        if self.font is None:
            return None
        elif callable(self.font):
            return self.font(tree_item)
        return self.font

    def get_foreground_color(self, tree_item):
        if self.foreground_color is None:
            return None
        elif callable(self.foreground_color):
            return self.foreground_color(tree_item)
        return self.foreground_color

    def get_background_color(self, tree_item):
        if self.background_color is None:
            return None
        elif callable(self.background_color):
            return self.background_color(tree_item)
        return self.background_color

    def get_decoration(self, tree_item):
        if self.decoration is None:
            return None
        elif callable(self.decoration):
            return self.decoration(tree_item)
        return self.decoration

    def get_alignment(self, tree_item) -> int:
        if self.alignment is None:
            return constants.ALIGN_LEFT
        elif callable(self.alignment):
            return self.alignment(tree_item)
        elif isinstance(self.alignment, str):
            return ALIGNMENTS[self.alignment]
        return self.alignment
