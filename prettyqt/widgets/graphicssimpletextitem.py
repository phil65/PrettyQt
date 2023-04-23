from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import get_repr


class GraphicsSimpleTextItem(
    widgets.AbstractGraphicsShapeItemMixin, QtWidgets.QGraphicsSimpleTextItem
):
    def __repr__(self):
        return get_repr(self, self.text())
