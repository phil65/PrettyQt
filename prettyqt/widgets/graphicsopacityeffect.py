from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QGraphicsOpacityEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsOpacityEffect(QtWidgets.QGraphicsOpacityEffect):
    def serialize_fields(self):
        return dict(opacity=self.opacity(), opacity_mask=self.get_opacity_mask())

    def __setstate__(self, state):
        self.setOpacity(state["opacity"])
        self.setOpacityMask(state["opacity_mask"])

    def get_opacity_mask(self) -> gui.Brush:
        return gui.Brush(self.opacityMask())
