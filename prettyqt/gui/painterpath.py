# -*- coding: utf-8 -*-

from typing import Tuple, Union

from qtpy import QtGui, QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


ELEMENT_TYPES = bidict(
    move_to_element=QtGui.QPainterPath.MoveToElement,
    line_to_element=QtGui.QPainterPath.LineToElement,
    curve_to_element=QtGui.QPainterPath.CurveToElement,
    curve_to_data_element=QtGui.QPainterPath.CurveToDataElement,
)

FILL_RULES = bidict(odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill)


class PainterPath(QtGui.QPainterPath):
    def serialize_fields(self):
        return dict(fill_rule=self.get_fill_rule(), elements=list(self))

    def __len__(self):
        return self.elementCount()

    def __getitem__(self, index: int):
        return self.elementAt(index)

    def __iter__(self):
        return iter(self.elementAt(i) for i in range(self.elementCount()))

    def __setitem__(self, index: int, value: Tuple[int, int]):
        self.setElementPositionAt(index, *value)

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, item: Union[QtCore.QPointF, QtCore.QRectF, "PainterPath"]):
        return self.contains(item)

    def add_rect(self, rect: Union[QtCore.QRectF, QtCore.QRect]):
        if isinstance(rect, QtCore.QRect):
            rect = QtCore.QRectF(rect)
        self.addRect(rect)

    def set_fill_rule(self, rule: str):
        """Set fill rule.

        Allowed values are "odd_even", "winding"

        Args:
            rule: fill rule to use

        Raises:
            InvalidParamError: fill rule does not exist
        """
        if rule not in FILL_RULES:
            raise InvalidParamError(rule, FILL_RULES)
        self.setFillRule(FILL_RULES[rule])

    def get_fill_rule(self) -> str:
        """Return current fill rule.

        Possible values: "odd_even", "winding"

        Returns:
            fill rule
        """
        return FILL_RULES.inv[self.fillRule()]

    def get_bounding_rect(self) -> core.RectF:
        return core.RectF(self.boundingRect())


if __name__ == "__main__":
    p = PainterPath(QtCore.QPoint(1, 1))
    print(list(p))
