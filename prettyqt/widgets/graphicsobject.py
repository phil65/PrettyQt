from typing import TYPE_CHECKING

from prettyqt import core, widgets


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _GraphicsObjectBase = QtWidgets.QGraphicsObject
else:
    _GraphicsObjectBase = object


class GraphicsObjectMixin(
    core.ObjectMixin, widgets.GraphicsItemMixin, _GraphicsObjectBase
):
    pass


class GraphicsObject(GraphicsObjectMixin, widgets.QGraphicsObject):
    """Base class for all graphics items that require signals, slots and properties."""
