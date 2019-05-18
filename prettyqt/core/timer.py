# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class Timer(QtCore.QTimer):

    @classmethod
    def single_shot(cls, callback):
        timer = cls()
        timer.timeout.connect(callback)
        timer.setSingleShot(True)
        return timer


Timer.__bases__[0].__bases__ = (core.Object,)
