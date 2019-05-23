# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


class GuiApplication(QtGui.QGuiApplication):
    pass


GuiApplication.__bases__[0].__bases__ = (core.CoreApplication,)
