# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui


QtWidgets.QStylePainter.__bases__ = (gui.Painter,)


class StylePainter(QtWidgets.QStylePainter):
    pass
