# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class Painter(QtGui.QPainter):

    def draw_image(self, point, frame_buffer):
        self.setCompositionMode(QtGui.QPainter.CompositionMode_SourceAtop)
        self.drawImage(point, frame_buffer)
        self.end()
