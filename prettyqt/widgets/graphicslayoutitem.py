from __future__ import annotations

from prettyqt.qt import QtWidgets
from prettyqt.utils import get_repr


class GraphicsLayoutItemMixin:
    def __repr__(self):
        return get_repr(self)


class GraphicsLayoutItem(GraphicsLayoutItemMixin, QtWidgets.QGraphicsLayoutItem):
    pass
