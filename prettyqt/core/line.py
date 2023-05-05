from __future__ import annotations

from collections.abc import Iterator
import math
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class Line(QtCore.QLine):
    def __repr__(self):
        return get_repr(self, self.get_p1(), self.get_p2())

    @property
    def _x1(self):
        return self.get_x1()

    @property
    def _y1(self):
        return self.y1()

    @property
    def _x2(self):
        return self.x2()

    @property
    def _y2(self):
        return self.y2()

    __match_args__ = ("_x1", "_y1", "_x2", "_y2")

    def __reduce__(self):
        return type(self), (self.get_p1(), self.get_p1())

    def __abs__(self) -> float:
        p = self.get_p2() - self.get_p1()
        return math.sqrt((p.x() * p.x()) + (p.y() * p.y()))

    def __reversed__(self) -> Line:
        return Line(self.get_p2(), self.get_p1())

    def __iter__(self) -> Iterator[core.Point]:
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: Literal[0, 1]) -> core.Point:
        if index == 0:
            return self.get_p1()
        elif index == 1:
            return self.get_p2()
        else:
            raise KeyError(index)

    def __setitem__(self, index: Literal[0, 1], value: datatypes.PointType):
        if index == 0:
            self.set_p1(value)
        elif index == 1:
            self.set_p2(value)
        else:
            raise KeyError(index)

    def get_p1(self) -> core.Point:
        return core.Point(self.p1())

    def set_p1(self, point: datatypes.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setP1(point)

    def get_p2(self) -> core.Point:
        return core.Point(self.p2())

    def set_p2(self, point: datatypes.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setP2(point)

    def get_center(self) -> core.Point:
        return core.Point(self.center())


if __name__ == "__main__":
    line = Line(core.Point(0, 0), core.Point(0, 0))
    print(bool(line))
    print(reversed(line))
