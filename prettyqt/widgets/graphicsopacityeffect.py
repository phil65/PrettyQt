from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QGraphicsOpacityEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsOpacityEffect(QtWidgets.QGraphicsOpacityEffect):
    def serialize_fields(self):
        return dict(opacity=self.opacity(), opacityMask=gui.Brush(self.opacityMask()))
