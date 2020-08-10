from qtpy import QtCore

from prettyqt import core


class Line(QtCore.QLine):
    def __getitem__(self, index):
        if index == 0:
            return core.Point(self.p1())
        elif index == 1:
            return core.Point(self.p2())

    def __setitem__(self, index, value):
        if index == 0:
            self.setP1(value)
        elif index == 1:
            self.setP2(value)
