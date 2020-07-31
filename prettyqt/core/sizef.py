# -*- coding: utf-8 -*-

from qtpy import QtCore


class SizeF(QtCore.QSizeF):
    def __repr__(self):
        return f"SizeF({self.width()}, {self.height()})"
