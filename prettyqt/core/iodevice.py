# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class IODevice(QtCore.QIODevice):
    pass


IODevice.__bases__[0].__bases__ = (core.Object,)
