from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class AbstractGraphicsShapeItemMixin(widgets.GraphicsItemMixin):
    pass


class AbstractGraphicsShapeItem(
    AbstractGraphicsShapeItemMixin, QtWidgets.QAbstractGraphicsShapeItem
):
    pass
