from qtpy import QtCore

from prettyqt import core


class LineF(QtCore.QLineF):
    def __repr__(self):
        return f"LineF({repr(self.get_p1())}, {repr(self.get_p1())})"

    def __reversed__(self):
        self[0], self[1] = self[1], self[0]
        return self

    def __abs__(self) -> float:
        return self.length()

    def __iter__(self):
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: int) -> core.PointF:
        if index == 0:
            return self.get_p1()
        elif index == 1:
            return self.get_p2()

    def __setitem__(self, index: int, value: core.PointF):
        if index == 0:
            self.setP1(value)
        elif index == 1:
            self.setP2(value)

    def get_p1(self) -> core.PointF:
        return core.PointF(self.p1())

    def get_p2(self) -> core.PointF:
        return core.PointF(self.p2())


if __name__ == "__main__":
    line = LineF(core.Point(0, 0), core.Point(2, 2))
    print(repr(line))
