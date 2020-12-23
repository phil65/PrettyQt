from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QGraphicsEffect.__bases__ = (core.Object,)


class GraphicsEffect(QtWidgets.QGraphicsEffect):
    def serialize_fields(self):
        return dict(enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setEnabled(state["enabled"])
