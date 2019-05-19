# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui


class StylePainter(QtWidgets.QStylePainter):
    pass


StylePainter.__bases__[0].__bases__ = (gui.Painter,)
