from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsPixmapItem.__bases__ = (widgets.GraphicsItem,)


class GraphicsPixmapItem(QtWidgets.QGraphicsPixmapItem):
    pass
