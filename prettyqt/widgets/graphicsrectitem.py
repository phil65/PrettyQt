from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import get_repr


class GraphicsRectItem(widgets.AbstractGraphicsShapeItemMixin, widgets.QGraphicsRectItem):
    """Rectangle item that you can add to a QGraphicsScene."""

    def __repr__(self):
        return get_repr(self, self.get_rect())

    def get_rect(self) -> core.RectF:
        return core.RectF(self.rect())

    def serialize_fields(self):
        return dict(rect=self.get_rect())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setRect(state["rect"])
