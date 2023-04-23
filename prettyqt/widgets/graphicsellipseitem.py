from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import get_repr


class GraphicsEllipseItem(
    widgets.AbstractGraphicsShapeItemMixin, QtWidgets.QGraphicsEllipseItem
):
    def __repr__(self):
        return get_repr(self, self.get_rect())

    def serialize_fields(self):
        return dict(
            rect=self.get_rect(),
            span_angle=self.spanAngle(),
            start_angle=self.startAngle(),
        )

    def get_rect(self) -> core.RectF:
        return core.RectF(self.rect())


if __name__ == "__main__":
    item = GraphicsEllipseItem()
    item.get_rect()
