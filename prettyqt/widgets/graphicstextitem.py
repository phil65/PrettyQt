from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import get_repr


class GraphicsTextItem(widgets.GraphicsObjectMixin, widgets.QGraphicsTextItem):
    """Text item that you can add to a QGraphicsScene to display formatted text."""

    def __repr__(self):
        return get_repr(self, self.toPlainText())
