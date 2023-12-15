from __future__ import annotations

from collections.abc import Iterator
import math
from typing import Literal, Self

from prettyqt import core
from prettyqt.utils import datatypes, get_repr


class Line(core.QLine):
    """Two-dimensional vector using integer precision."""

    def __repr__(self):
        return get_repr(self, self.get_p1(), self.get_p2())

    @property
    def _x1(self) -> int:
        return self.get_x1()

    @property
    def _y1(self) -> int:
        return self.y1()

    @property
    def _x2(self) -> int:
        return self.x2()

    @property
    def _y2(self) -> int:
        return self.y2()

    __match_args__ = ("_x1", "_y1", "_x2", "_y2")

    def __reduce__(self):
        return type(self), (self.get_p1(), self.get_p1())

    def __abs__(self) -> float:
        p = self.get_p2() - self.get_p1()
        return math.sqrt((p.x() * p.x()) + (p.y() * p.y()))

    def __reversed__(self) -> Self:
        return type(self)(self.get_p2(), self.get_p1())

    def __iter__(self) -> Iterator[core.Point]:
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: Literal[0, 1]) -> core.Point:
        match index:
            case 0:
                return self.get_p1()
            case 1:
                return self.get_p2()
            case _:
                raise IndexError(index)

    def __setitem__(self, index: Literal[0, 1], value: datatypes.PointType):
        match index:
            case 0:
                self.set_p1(value)
            case 1:
                self.set_p2(value)
            case _:
                raise KeyError(index)

    def get_p1(self) -> core.Point:
        return core.Point(self.p1())

    def set_p1(self, point: datatypes.PointType):
        self.setP1(datatypes.to_point(point))

    def get_p2(self) -> core.Point:
        return core.Point(self.p2())

    def set_p2(self, point: datatypes.PointType):
        self.setP2(datatypes.to_point(point))

    def get_center(self) -> core.Point:
        return core.Point(self.center())


if __name__ == "__main__":
    line = Line(core.Point(0, 0), core.Point(0, 0))
