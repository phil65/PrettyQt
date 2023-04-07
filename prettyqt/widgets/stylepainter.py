from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


class StylePainter(gui.PainterMixin, QtWidgets.QStylePainter):
    def draw_complex_control(
        self,
        control: widgets.style.ComplexControlStr,
        option: QtWidgets.QStyleOptionComplex,
    ):
        self.drawComplexControl(widgets.style.COMPLEX_CONTROL[control], option)
