from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QGraphicsColorizeEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsColorizeEffect(QtWidgets.QGraphicsColorizeEffect):
    def serialize_fields(self):
        return dict(strength=self.strength(), color=gui.Color(self.color()))
