# -*- coding: utf-8 -*-

from qtpy import QtCore


class Point(QtCore.QPoint):
    def __repr__(self):
        return f"Point(x={self.x()}, y={self.y()})"
