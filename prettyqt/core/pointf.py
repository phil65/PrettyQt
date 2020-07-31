# -*- coding: utf-8 -*-

from qtpy import QtCore


class PointF(QtCore.QPointF):
    def __repr__(self):
        return f"PointF(x={self.x()}, y={self.y()})"
