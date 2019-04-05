# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class Color(QtGui.QColor):

    def set_color(self, color):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)
