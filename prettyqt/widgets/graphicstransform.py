from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


class GraphicsTransformMixin(core.ObjectMixin):
    pass


class GraphicsTransform(GraphicsTransformMixin, QtWidgets.QGraphicsTransform):
    pass


if __name__ == "__main__":
    transform = GraphicsTransform()
