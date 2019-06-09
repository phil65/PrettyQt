# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict


WEIGHTS = bidict(thin=QtGui.QFont.Thin,
                 light=QtGui.QFont.Light,
                 medium=QtGui.QFont.Medium,
                 bold=QtGui.QFont.Bold)


class TextCharFormat(QtGui.QTextCharFormat):

    def set_foreground_color(self, color_name):
        color = gui.Color()
        color.set_color(color_name)
        self.setForeground(color)

    def set_font_weight(self, weight: str):
        """sets the font weight

        Valid values are "thin", "light", "medium" and "bold"

        Args:
            weight: font weight

        Raises:
            ValueError: invalid font weight
        """
        if weight not in WEIGHTS:
            raise ValueError("Invalid font weight")
        self.setFontWeight(WEIGHTS[weight])

    def get_font_weight(self) -> str:
        """get current font weight

        Possible values are "thin", "light", "medium" or "bold"

        Returns:
            current font weight
        """
        return WEIGHTS.inv[self.fontWeight()]
