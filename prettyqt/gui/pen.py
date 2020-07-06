# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtGui

from prettyqt.utils import colors


class Pen(QtGui.QPen):
    def set_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.setColor(color)
