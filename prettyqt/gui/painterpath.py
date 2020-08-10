# -*- coding: utf-8 -*-

from typing import Tuple, Union

from qtpy import QtGui, QtCore

from prettyqt.utils import bidict


ELEMENT_TYPES = bidict(
    move_to_element=QtGui.QPainterPath.MoveToElement,
    line_to_element=QtGui.QPainterPath.LineToElement,
    curve_to_element=QtGui.QPainterPath.CurveToElement,
    curve_to_data_element=QtGui.QPainterPath.CurveToDataElement,
)


class PainterPath(QtGui.QPainterPath):
    def __len__(self):
        return self.elementCount()

    def __getitem__(self, index: int):
        return self.elementAt(index)

    def __setitem__(self, index: int, value: Tuple[int, int]):
        self.setElementPositionAt(index, *value)

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, item: Union[QtCore.QPointF, QtCore.QRectF, "PainterPath"]):
        return self.contains(item)
