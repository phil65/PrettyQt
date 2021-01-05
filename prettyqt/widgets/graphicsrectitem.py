from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsRectItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_rect())})"

    def get_rect(self):
        return core.RectF(self.rect())

    def serialize_fields(self):
        return dict(rect=self.get_rect())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setRect(state["rect"])
