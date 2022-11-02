from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, types


ELEMENT_TYPES = bidict(
    move_to_element=QtGui.QPainterPath.ElementType.MoveToElement,
    line_to_element=QtGui.QPainterPath.ElementType.LineToElement,
    curve_to_element=QtGui.QPainterPath.ElementType.CurveToElement,
    curve_to_data_element=QtGui.QPainterPath.ElementType.CurveToDataElement,
)

ElementTypeStr = Literal[
    "move_to_element", "line_to_element", "curve_to_element", "curve_to_data_element"
]


class PainterPath(QtGui.QPainterPath):
    def serialize_fields(self):
        return dict(fill_rule=self.get_fill_rule(), elements=list(self))

    def __len__(self):
        return self.elementCount()

    def __getitem__(self, index: int) -> QtGui.QPainterPath.Element:
        return self.elementAt(index)

    def __iter__(self) -> Iterator[QtGui.QPainterPath.Element]:
        return iter(self.elementAt(i) for i in range(self.elementCount()))

    def __setitem__(self, index: int, value: tuple[int, int]):
        self.setElementPositionAt(index, *value)

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, item: QtCore.QPointF | QtCore.QRectF | QtGui.QPainterPath):
        return self.contains(item)

    def add_rect(self, rect: types.RectType | types.RectFType):
        if isinstance(rect, QtCore.QRect):
            rect = QtCore.QRectF(rect)
        elif isinstance(rect, tuple):
            rect = QtCore.QRectF(*rect)
        self.addRect(rect)

    def set_fill_rule(self, rule: constants.FillRuleStr):
        """Set fill rule.

        Args:
            rule: fill rule to use

        Raises:
            InvalidParamError: fill rule does not exist
        """
        if rule not in constants.FILL_RULE:
            raise InvalidParamError(rule, constants.FILL_RULE)
        self.setFillRule(constants.FILL_RULE[rule])

    def get_fill_rule(self) -> constants.FillRuleStr:
        """Return current fill rule.

        Returns:
            fill rule
        """
        return constants.FILL_RULE.inverse[self.fillRule()]

    def get_bounding_rect(self) -> core.RectF:
        return core.RectF(self.boundingRect())


if __name__ == "__main__":
    p = PainterPath(QtCore.QPoint(1, 1))
    print(type(p[0]))
