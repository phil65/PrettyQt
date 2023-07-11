from __future__ import annotations

from prettyqt import gui, widgets


class StylePainter(gui.PainterMixin, widgets.QStylePainter):
    """Convenience class for drawing QStyle elements inside a widget."""

    def draw_complex_control(
        self,
        control: widgets.style.ComplexControlStr,
        option: widgets.QStyleOptionComplex,
    ):
        self.drawComplexControl(widgets.style.COMPLEX_CONTROL[control], option)
