from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class GraphicsTextItem(widgets.GraphicsObjectMixin, QtWidgets.QGraphicsTextItem):
    def __repr__(self):
        return f"{type(self).__name__}({self.toPlainText()!r})"
