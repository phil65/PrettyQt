# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class FileDevice(QtCore.QFileDevice):
    pass


FileDevice.__bases__[0].__bases__ = (core.IODevice,)
