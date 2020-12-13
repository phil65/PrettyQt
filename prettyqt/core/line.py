from __future__ import annotations

from typing import Literal, Iterator

import math

from qtpy import QtCore

from prettyqt import core


class Line(QtCore.QLine):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_p1())}, {repr(self.get_p2())})"

    def __reduce__(self):
        return (self.__class__, (self.get_p1(), self.get_p1()))

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

    def __setitem__(self, index: Literal[0, 1], value: QtCore.Point):
        if index == 0:
            self.setP1(value)
        elif index == 1:
            self.setP2(value)
        else:
            raise KeyError(index)

    def get_p1(self) -> core.Point:
        return core.Point(self.p1())

    def get_p2(self) -> core.Point:
        return core.Point(self.p2())


if __name__ == "__main__":
    line = Line(core.Point(0, 0), core.Point(2, 2))
    print(reversed(line))
