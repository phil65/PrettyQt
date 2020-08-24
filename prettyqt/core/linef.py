from qtpy import QtCore

from prettyqt import core


class LineF(QtCore.QLineF):
    def __repr__(self):
        return f"LineF({repr(self.get_p1())}, {repr(self.get_p1())})"

    def __iter__(self):
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index):
        if index == 0:
            return self.get_p1()
        elif index == 1:
            return self.get_p2()

    def __setitem__(self, index, value):
        if index == 0:
            self.setP1(value)
        elif index == 1:
            self.setP2(value)

    def get_p1(self):
        return core.PointF(self.p1())

    def get_p2(self):
        return core.PointF(self.p2())


if __name__ == "__main__":
    line = LineF(core.Point(0, 0), core.Point(2, 2))
    print(repr(line))
