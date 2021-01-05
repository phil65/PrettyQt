from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsTransform.__bases__ = (core.Object,)


class GraphicsTransform(QtWidgets.QGraphicsTransform):
    pass


if __name__ == "__main__":
    transform = GraphicsTransform()
