from typing import TYPE_CHECKING

from prettyqt import widgets


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _AbstractGraphicsShapeItemBase = QtWidgets.QAbstractGraphicsShapeItem
else:
    _AbstractGraphicsShapeItemBase = object


class AbstractGraphicsShapeItemMixin(
    widgets.GraphicsItemMixin, _AbstractGraphicsShapeItemBase
):
    pass


class AbstractGraphicsShapeItem(
    AbstractGraphicsShapeItemMixin, widgets.QAbstractGraphicsShapeItem
):
    """Common base for all path items."""
