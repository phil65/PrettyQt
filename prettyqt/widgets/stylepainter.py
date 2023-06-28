from __future__ import annotations

from prettyqt import gui, widgets


class StylePainter(gui.PainterMixin, widgets.QStylePainter):
    def draw_complex_control(
        self,
        control: widgets.style.ComplexControlStr,
        option: widgets.QStyleOptionComplex,
    ):
        self.drawComplexControl(widgets.style.COMPLEX_CONTROL[control], option)
