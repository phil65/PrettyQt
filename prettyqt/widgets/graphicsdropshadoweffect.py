from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsDropShadowEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsDropShadowEffect(QtWidgets.QGraphicsDropShadowEffect):
    def serialize_fields(self):
        offset = self.offset()
        return dict(
            blur_radius=self.blurRadius(),
            color=gui.Color(self.color()),
            offset=(offset.x(), offset.y()),
        )
