# -*- coding: utf-8 -*-

from qtpy import QtCore


class Rect(QtCore.QRect):
    def __repr__(self):
        return f"Rect({self.x()}, {self.y()}, {self.width()}, {self.height()})"


if __name__ == "__main__":
    rect = Rect(0, 2, 5, 5)
    print(repr(rect))
