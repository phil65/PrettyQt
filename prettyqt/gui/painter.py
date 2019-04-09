# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore

COLORS = dict(transparent=QtCore.Qt.transparent)

PEN_TYPES = dict(none=QtCore.Qt.NoPen)

COMP_MODES = dict(source_at_top=QtGui.QPainter.CompositionMode_SourceAtop)


class Painter(QtGui.QPainter):

    def draw_image(self, point, frame_buffer):
        self.set_composition_mode("source_at_top")
        self.drawImage(point, frame_buffer)
        self.end()

    def use_antialiasing(self):
        self.setRenderHint(self.Antialiasing, True)

    def fill_rect(self, rect, color):
        if color not in COLORS:
            raise ValueError("Invalid value for color.")
        self.fillRect(rect, COLORS[color])

    def set_pen(self, pen_type):
        if pen_type not in PEN_TYPES:
            raise ValueError("Invalid value for pen_type.")
        self.setPen(PEN_TYPES[pen_type])

    def set_color(self, color):
        color = QtGui.QColor(color)
        self.setPen(color)

    def set_composition_mode(self, mode):
        if mode not in COMP_MODES:
            raise ValueError("Invalid value for composition mode.")
        self.setCompositionMode(COMP_MODES[mode])
