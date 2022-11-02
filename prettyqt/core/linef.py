from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import types


class LineF(QtCore.QLineF):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_p1())}, {repr(self.get_p1())})"

    def __reduce__(self):
        return type(self), (self.get_p1(), self.get_p1())

    def __reversed__(self):
        return LineF(self.get_p2(), self.get_p1())

    def __abs__(self) -> float:
        return self.length()

    def __iter__(self) -> Iterator[core.PointF]:
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: Literal[0, 1]) -> core.PointF:
        if index == 0:
            return self.get_p1()
        elif index == 1:
            return self.get_p2()
        else:
            raise KeyError(index)

    def __setitem__(self, index: Literal[0, 1], value: types.PointFType):
        if index == 0:
            self.set_p1(value)
        elif index == 1:
            self.set_p2(value)
        else:
            raise KeyError(index)

    def set_p1(self, point: types.PointFType):
        self.setP1(core.PointF(*point) if isinstance(point, tuple) else point)

    def get_p1(self) -> core.PointF:
        return core.PointF(self.p1())

    def set_p2(self, point: types.PointFType):
        self.setP2(core.PointF(*point) if isinstance(point, tuple) else point)

    def get_p2(self) -> core.PointF:
        return core.PointF(self.p2())

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_normal_vector(self) -> LineF:
        return LineF(self.normalVector())

    def get_unit_vector(self) -> LineF:
        return LineF(self.unitVector())

    def to_line(self) -> core.Line:
        return core.Line(self.toLine())


if __name__ == "__main__":
    line = LineF(core.Point(0, 0), core.Point(2, 2))
    print(repr(line))
    for p in line:
        print(p)
