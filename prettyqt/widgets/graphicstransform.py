from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtWidgets


if TYPE_CHECKING:
    _GraphicsTransformBase = QtWidgets.QGraphicsTransform
else:
    _GraphicsTransformBase = object


class GraphicsTransformMixin(core.ObjectMixin, _GraphicsTransformBase):
    pass


class GraphicsTransform(GraphicsTransformMixin, QtWidgets.QGraphicsTransform):
    """Abstract base class for building advanced transformations on QGraphicsItems."""


if __name__ == "__main__":
    transform = GraphicsTransform()
