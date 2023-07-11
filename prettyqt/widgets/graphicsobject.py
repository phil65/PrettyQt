from __future__ import annotations

from prettyqt import core, widgets


class GraphicsObjectMixin(core.ObjectMixin, widgets.GraphicsItemMixin):
    pass


class GraphicsObject(GraphicsObjectMixin, widgets.QGraphicsObject):
    """Base class for all graphics items that require signals, slots and properties."""
