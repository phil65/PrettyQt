from __future__ import annotations

from prettyqt.qt import QtWidgets


class GraphicsLayoutItemMixin:
    def __repr__(self):
        return f"{type(self).__name__}()"


class GraphicsLayoutItem(GraphicsLayoutItemMixin, QtWidgets.QGraphicsLayoutItem):
    pass
