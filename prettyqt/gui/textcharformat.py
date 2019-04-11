# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class TextCharFormat(QtGui.QTextCharFormat):

    def set_foreground_color(self, color_name):
        color = gui.Color()
        color.set_color(color_name)
        self.setForeground(color)

    def set_font_weight(self, weight):
        WEIGHTS = dict(thin=QtGui.QFont.Thin,
                       light=QtGui.QFont.Light,
                       medium=QtGui.QFont.Medium,
                       bold=QtGui.QFont.Bold)
        if weight not in WEIGHTS:
            raise ValueError("Invalid font weight")
        self.setFontWeight(WEIGHTS[weight])
