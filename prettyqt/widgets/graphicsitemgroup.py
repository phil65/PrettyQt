from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsItemGroup.__bases__ = (widgets.GraphicsItem,)


class GraphicsItemGroup(QtWidgets.QGraphicsItemGroup):
    pass
