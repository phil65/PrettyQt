# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class Palette(QtGui.QPalette):

    def highlight_inactive(self):
        color = self.color(self.Active, self.Highlight)
        self.setColor(self.Inactive, self.Highlight, color)
