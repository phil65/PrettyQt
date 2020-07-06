# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore


class Size(QtCore.QSize):
    def __repr__(self):
        return f"Size({self.width()}, {self.height()})"
