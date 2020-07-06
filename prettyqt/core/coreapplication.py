# -*- coding: utf-8 -*-
"""
"""

from typing import Callable

from qtpy import QtCore

from prettyqt import core


QtCore.QCoreApplication.__bases__ = (core.Object,)


class CoreApplication(QtCore.QCoreApplication):
    @classmethod
    def call_on_exit(cls, func: Callable):
        cls.instance().aboutToQuit.connect(func)
