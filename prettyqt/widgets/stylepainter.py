from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QStylePainter.__bases__ = (gui.Painter,)


class StylePainter(QtWidgets.QStylePainter):
    def draw_complex_control(
        self,
        control: widgets.style.ComplexControlStr,
        option: QtWidgets.QStyleOptionComplex,
    ):
        self.drawComplexControl(widgets.style.COMPLEX_CONTROL[control], option)
