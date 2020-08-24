# -*- coding: utf-8 -*-

from qtpy import QtCore


class RectF(QtCore.QRectF):
    def __repr__(self):
        return f"RectF({self.x()}, {self.y()}, {self.width()}, {self.height()})"


if __name__ == "__main__":
    rect = RectF(0, 2, 5, 5)
    print(repr(rect))
