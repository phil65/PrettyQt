# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import gui, widgets

COMPLEX_CONTROLS = widgets.style.COMPLEX_CONTROLS

QtWidgets.QStylePainter.__bases__ = (gui.Painter,)


class StylePainter(QtWidgets.QStylePainter):
    def draw_complex_control(self, control: str, option: QtWidgets.QStyleOptionComplex):
        self.drawComplexControl(COMPLEX_CONTROLS[control], option)
