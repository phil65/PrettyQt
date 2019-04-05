# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore


class KeySequence(QtGui.QKeySequence):

    def __str__(self):
        return self.toString()

    def set_color(self, color):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)

    @classmethod
    def from_key_and_mod(cls, key, mod):
        mods = {QtCore.Qt.ShiftModifier: QtCore.Qt.SHIFT,
                QtCore.Qt.ControlModifier: QtCore.Qt.CTRL,
                QtCore.Qt.AltModifier: QtCore.Qt.ALT,
                QtCore.Qt.MetaModifier: QtCore.Qt.META}
        for k, v in mods.items():
            if mod & k:
                key += v
        return cls(key)
