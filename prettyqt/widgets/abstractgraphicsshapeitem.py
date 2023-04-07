from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


class AbstractGraphicsShapeItemMixin(
    widgets.GraphicsItemMixin,
):
    def serialize_fields(self):
        return dict(brush=gui.Brush(self.brush()), pen=gui.Pen(self.pen()))


class AbstractGraphicsShapeItem(
    AbstractGraphicsShapeItemMixin, QtWidgets.QAbstractGraphicsShapeItem
):
    pass
