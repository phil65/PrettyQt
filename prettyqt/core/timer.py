# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QTimer.__bases__ = (core.Object,)


class Timer(QtCore.QTimer):
    @classmethod
    def single_shot(cls, callback):
        timer = cls()
        timer.timeout.connect(callback)
        timer.setSingleShot(True)
        return timer
