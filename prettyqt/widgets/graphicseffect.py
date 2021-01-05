from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsEffect.__bases__ = (core.Object,)


class GraphicsEffect(QtWidgets.QGraphicsEffect):
    def serialize_fields(self):
        return dict(enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setEnabled(state["enabled"])
