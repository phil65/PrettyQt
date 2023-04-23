from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import get_repr


class GraphicsTextItem(widgets.GraphicsObjectMixin, QtWidgets.QGraphicsTextItem):
    def __repr__(self):
        return get_repr(self, self.toPlainText())
