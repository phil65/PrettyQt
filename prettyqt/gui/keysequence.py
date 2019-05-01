# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtGui


class KeySequence(QtGui.QKeySequence):

    def __str__(self):
        return self.toString()

    @classmethod
    def to_shortcut_str(cls, key, mod=0):
        mods = {QtCore.Qt.ShiftModifier: QtCore.Qt.SHIFT,
                QtCore.Qt.ControlModifier: QtCore.Qt.CTRL,
                QtCore.Qt.AltModifier: QtCore.Qt.ALT,
                QtCore.Qt.MetaModifier: QtCore.Qt.META}
        for k, v in mods.items():
            if mod & k:
                key += v
        return str(cls(key))
