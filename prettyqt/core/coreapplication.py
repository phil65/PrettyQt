# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class CoreApplication(QtCore.QCoreApplication):
    pass


CoreApplication.__bases__[0].__bases__ = (core.Object,)
