from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsPathItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsPathItem(QtWidgets.QGraphicsPathItem):
    pass
