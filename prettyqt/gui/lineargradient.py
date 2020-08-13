# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui


QtGui.QLinearGradient.__bases__ = (gui.Gradient,)


class LinearGradient(QtGui.QLinearGradient):
    pass
