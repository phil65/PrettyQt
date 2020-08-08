# -*- coding: utf-8 -*-

from typing import Callable, Optional, Union
from dataclasses import dataclass

from qtpy import QtCore, QtGui

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200

ALIGN_LEFT = int(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
ALIGN_RIGHT = int(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
ALIGN_CENTER = int(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)


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

    def get_name(self):
        return self.name

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

    def get_alignment(self, tree_item):
        if self.alignment is None:
            return ALIGN_LEFT
        elif callable(self.alignment):
            return self.alignment(tree_item)
        return self.alignment
