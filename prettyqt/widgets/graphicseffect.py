from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QGraphicsEffect.__bases__ = (core.Object,)


class GraphicsEffect(QtWidgets.QGraphicsEffect):
    def serialize_fields(self):
        return dict(enabled=self.isEnabled())
