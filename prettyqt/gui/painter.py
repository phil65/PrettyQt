# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtCore, QtGui

from prettyqt import core, gui

PEN_TYPES = bidict(dict(none=QtCore.Qt.NoPen))

COMP_MODES = bidict(dict(source_at_top=QtGui.QPainter.CompositionMode_SourceAtop))

PATTERNS = bidict(dict(solid=QtCore.Qt.SolidPattern,
                       none=QtCore.Qt.NoBrush,
                       cross=QtCore.Qt.CrossPattern,
                       linear_gradient=QtCore.Qt.LinearGradientPattern,
                       radial_gradient=QtCore.Qt.RadialGradientPattern))


class Painter(QtGui.QPainter):

    def draw_image(self, point, frame_buffer):
        self.set_composition_mode("source_at_top")
        self.drawImage(point, frame_buffer)
        self.end()

    def use_antialiasing(self):
        self.setRenderHint(self.Antialiasing, True)

    def fill_rect(self, rect, color, pattern="solid"):
        if isinstance(rect, tuple):
            rect = core.Rect(*rect)
        if isinstance(color, str):
            if color not in gui.Color.colorNames():
                raise ValueError("Invalid value for color.")
            color = gui.Color(color)
        if pattern != "solid":
            color = gui.Brush(color, PATTERNS[pattern])
        self.fillRect(rect, color)

    def set_pen(self, pen_type: str):
        if pen_type not in PEN_TYPES:
            raise ValueError("Invalid value for pen_type.")
        self.setPen(PEN_TYPES[pen_type])

    def get_pen(self) -> str:
        return PEN_TYPES.inv[self.pen()]

    def set_color(self, color):
        color = QtGui.QColor(color)
        self.setPen(color)

    def set_composition_mode(self, mode: str):
        if mode not in COMP_MODES:
            raise ValueError("Invalid value for composition mode.")
        self.setCompositionMode(COMP_MODES[mode])

    def get_composition_mode(self) -> str:
        return COMP_MODES.inv[self.compositionMode()]

    def draw_text(self, x, y, width, height, alignment, text):
        # TODO
        alignment = QtCore.Qt.AlignRight
        self.drawText(x, y, width, height, alignment, text)
