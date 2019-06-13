# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


QtGui.QGuiApplication.__bases__ = (core.CoreApplication,)


class GuiApplication(QtGui.QGuiApplication):
    pass
