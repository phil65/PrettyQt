# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict
from qtpy import QtGui

from prettyqt import gui


WEIGHTS = bidict(dict(thin=QtGui.QFont.Thin,
                      light=QtGui.QFont.Light,
                      medium=QtGui.QFont.Medium,
                      bold=QtGui.QFont.Bold))


class TextCharFormat(QtGui.QTextCharFormat):

    def set_foreground_color(self, color_name):
        color = gui.Color()
        color.set_color(color_name)
        self.setForeground(color)

    def set_font_weight(self, weight: str):
        if weight not in WEIGHTS:
            raise ValueError("Invalid font weight")
        self.setFontWeight(WEIGHTS[weight])

    def get_font_weight(self) -> str:
        return WEIGHTS.inv[self.fontWeight()]
