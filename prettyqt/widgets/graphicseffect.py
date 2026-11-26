from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtWidgets


if TYPE_CHECKING:
    _GraphicsEffectBase = QtWidgets.QGraphicsEffect
else:
    _GraphicsEffectBase = object


class GraphicsEffectMixin(core.ObjectMixin, _GraphicsEffectBase):
    pass


class GraphicsEffect(GraphicsEffectMixin, QtWidgets.QGraphicsEffect):
    """The base class for all graphics effects."""
