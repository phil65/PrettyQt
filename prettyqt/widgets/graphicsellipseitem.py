from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import get_repr


class GraphicsEllipseItem(
    widgets.AbstractGraphicsShapeItemMixin, widgets.QGraphicsEllipseItem
):
    def __repr__(self):
        return get_repr(self, self.get_rect())

    def get_rect(self) -> core.RectF:
        return core.RectF(self.rect())


if __name__ == "__main__":
    item = GraphicsEllipseItem()
    item.get_rect()
