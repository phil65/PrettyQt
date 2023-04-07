from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class GraphicsSimpleTextItem(
    widgets.AbstractGraphicsShapeItemMixin, QtWidgets.QGraphicsSimpleTextItem
):
    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"
