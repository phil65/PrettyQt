# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QThreadPool.__bases__ = (core.Object,)


class ThreadPool(QtCore.QThreadPool):
    pass
