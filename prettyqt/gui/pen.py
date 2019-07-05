# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class Pen(QtGui.QPen):

    def set_color(self, color):
        if isinstance(color, str):
            color = gui.Color(color)
        self.setColor(color)
