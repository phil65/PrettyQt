from __future__ import annotations

from prettyqt import widgets


class AbstractGraphicsShapeItemMixin(widgets.GraphicsItemMixin):
    pass


class AbstractGraphicsShapeItem(
    AbstractGraphicsShapeItemMixin, widgets.QAbstractGraphicsShapeItem
):
    """Common base for all path items."""
