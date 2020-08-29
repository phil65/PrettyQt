import math

from qtpy import QtCore

from prettyqt import core


class Line(QtCore.QLine):
    def __repr__(self):
        return f"Line({repr(self.get_p1())}, {repr(self.get_p2())})"

    def __abs__(self) -> float:
        p = self.get_p2() - self.get_p1()
        return math.sqrt((p.x() * p.x()) + (p.y() * p.y()))

    def __reversed__(self):
        self[0], self[1] = self[1], self[0]
        return self

    def __iter__(self):
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: int) -> core.Point:
        if index == 0:
            return self.get_p1()
        elif index == 1:
            return self.get_p2()

    def __setitem__(self, index: int, value: QtCore.QPoint):
        if index == 0:
            self.setP1(value)
        elif index == 1:
            self.setP2(value)

    def get_p1(self) -> core.Point:
        return core.Point(self.p1())

    def get_p2(self) -> core.Point:
        return core.Point(self.p2())


if __name__ == "__main__":
    line = Line(core.Point(0, 0), core.Point(2, 2))
    print(reversed(line))
