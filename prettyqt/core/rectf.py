# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore


class RectF(QtCore.QRectF):
    def __repr__(self):
        return f"RectF({self.x()}, {self.y()}, {self.width()}, {self.height()})"
