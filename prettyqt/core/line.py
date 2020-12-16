from __future__ import annotations

import math
from typing import Iterator, Literal, Tuple, Union

from qtpy import QtCore

from prettyqt import core


class Line(QtCore.QLine):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_p1())}, {repr(self.get_p2())})"

    def __reduce__(self):
        return self.__class__, (self.get_p1(), self.get_p1())

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

    def __setitem__(
        self, index: Literal[0, 1], value: Union[QtCore.Point, Tuple[int, int]]
    ):
        if index == 0:
            self.set_p1(value)
        elif index == 1:
            self.set_p2(value)
        else:
            raise KeyError(index)

    def get_p1(self) -> core.Point:
        return core.Point(self.p1())

    def set_p1(self, point: Union[QtCore.QPoint, Tuple[int, int]]):
        if isinstance(point, tuple):
            point = core.PointF(*point)
        self.setP1(point)

    def get_p2(self) -> core.Point:
        return core.Point(self.p2())

    def set_p2(self, point: Union[QtCore.QPoint, Tuple[int, int]]):
        if isinstance(point, tuple):
            point = core.PointF(*point)
        self.setP2(point)

    def get_center(self) -> core.Point:
        return core.Point(self.center())


if __name__ == "__main__":
    line = Line(core.Point(0, 0), core.Point(0, 0))
    print(bool(line))
    print(reversed(line))
