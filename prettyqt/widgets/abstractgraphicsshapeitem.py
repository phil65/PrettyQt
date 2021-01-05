from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QAbstractGraphicsShapeItem.__bases__ = (widgets.GraphicsItem,)


class AbstractGraphicsShapeItem(QtWidgets.QAbstractGraphicsShapeItem):
    def serialize_fields(self):
        return dict(brush=gui.Brush(self.brush()), pen=gui.Pen(self.pen()))
