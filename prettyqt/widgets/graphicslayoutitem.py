from __future__ import annotations

from prettyqt.qt import QtWidgets


class GraphicsLayoutItem(QtWidgets.QGraphicsLayoutItem):
    def __repr__(self):
        return f"{type(self).__name__}()"
