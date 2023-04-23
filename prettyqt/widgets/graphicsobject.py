from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class GraphicsObjectMixin(core.ObjectMixin, widgets.GraphicsItemMixin):
    pass


class GraphicsObject(GraphicsObjectMixin, QtWidgets.QGraphicsObject):
    pass
