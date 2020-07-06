# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore


class Rect(QtCore.QRect):
    def __repr__(self):
        return f"Rect({self.x()}, {self.y()}, {self.width()}, {self.height()})"
