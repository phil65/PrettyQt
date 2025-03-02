from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, datatypes


if TYPE_CHECKING:
    from collections.abc import Iterator


ElementTypeStr = Literal[
    "move_to_element", "line_to_element", "curve_to_element", "curve_to_data_element"
]

ELEMENT_TYPES: bidict[ElementTypeStr, QtGui.QPainterPath.ElementType] = bidict(
    move_to_element=QtGui.QPainterPath.ElementType.MoveToElement,
    line_to_element=QtGui.QPainterPath.ElementType.LineToElement,
    curve_to_element=QtGui.QPainterPath.ElementType.CurveToElement,
    curve_to_data_element=QtGui.QPainterPath.ElementType.CurveToDataElement,
)


class PainterPath(QtGui.QPainterPath):
    def __len__(self):
        return self.elementCount()

    def __getitem__(self, index: int) -> QtGui.QPainterPath.Element:
        return self.elementAt(index)

    def __iter__(self) -> Iterator[QtGui.QPainterPath.Element]:
        return iter(self.elementAt(i) for i in range(self.elementCount()))

    def __setitem__(self, index: int, value: tuple[int, int]):
        self.setElementPositionAt(index, *value)

    def __iadd__(self, other):
        if not isinstance(
            other,
            core.QPoint | core.QRect | QtGui.QPainterPath | QtGui.QRegion,
        ):
            raise TypeError(other)
        self.add(other)
        return self

    def add(self, other: core.QPoint | core.QRect | QtGui.QPainterPath | QtGui.QRegion):
        match other:
            case QtGui.QPolygonF():
                self.addPolygon(other)
            case QtGui.QPainterPath():
                self.addPath(other)
            case core.QRect():
                self.addRect(other)
            case QtGui.QRegion():
                self.addRegion(other)

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, item: core.QPointF | core.QRectF | QtGui.QPainterPath):
        return self.contains(item)

    def add_rect(self, rect: datatypes.RectType | datatypes.RectFType):
        self.addRect(datatypes.to_rectf(rect))

    def set_fill_rule(self, rule: constants.FillRuleStr):
        """Set fill rule.

        Args:
            rule: fill rule to use
        """
        self.setFillRule(constants.FILL_RULE[rule])

    def get_fill_rule(self) -> constants.FillRuleStr:
        """Return current fill rule.

        Returns:
            fill rule
        """
        return constants.FILL_RULE.inverse[self.fillRule()]

    def get_bounding_rect(self) -> core.RectF:
        return core.RectF(self.boundingRect())

    def get_simplified(self) -> PainterPath:
        return PainterPath(self.simplified())

    def to_reversed(self) -> PainterPath:
        return PainterPath(self.toReversed())

    @classmethod
    def create_star(cls, size: int):
        path = cls()
        star_center_x = size / 2
        star_center_y = size / 2
        radius_outer = size * 0.35
        golden_ratio = (1 + math.sqrt(5)) / 2
        radius_inner = radius_outer / (1 + golden_ratio)
        theta_start = math.pi / 2
        theta_inc = (2 * math.pi) / 10
        for n in range(11):
            theta = theta_start + (n * theta_inc)
            theta = theta % (2 * math.pi)
            if n % 2 == 0:
                x = radius_outer * math.cos(theta)
                y = radius_outer * math.sin(theta)

            else:
                x = radius_inner * math.cos(theta)
                y = radius_inner * math.sin(theta)

            x_adj = star_center_x - x
            y_adj = star_center_y - y + 3
            if n == 0:
                path.moveTo(x_adj, y_adj)
            else:
                path.lineTo(x_adj, y_adj)

        return path


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()

    class Test(widgets.Widget):
        def paintEvent(self, event):
            with gui.Painter(self) as painter:
                painter.drawPath(gui.PainterPath.create_star(400, 200))

    p = PainterPath.create_star(400, 200)
    p += core.QPoint(1, 1)

    t = Test()
    t.show()
    app.exec()
