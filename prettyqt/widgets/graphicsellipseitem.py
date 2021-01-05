from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsEllipseItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsEllipseItem(QtWidgets.QGraphicsEllipseItem):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_rect())})"

    def serialize_fields(self):
        return dict(
            rect=self.get_rect(),
            span_angle=self.spanAngle(),
            start_angle=self.startAngle(),
        )

    def get_rect(self) -> core.Rect:
        return core.Rect(self.rect())
