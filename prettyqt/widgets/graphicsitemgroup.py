from __future__ import annotations

from prettyqt import widgets


class GraphicsItemGroup(widgets.GraphicsItemMixin, widgets.QGraphicsItemGroup):
    """Container that treats a group of items as a single item."""
