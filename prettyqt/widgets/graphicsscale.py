from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsScale.__bases__ = (widgets.GraphicsTransform,)


class GraphicsScale(QtWidgets.QGraphicsScale):
    pass


if __name__ == "__main__":
    transform = GraphicsScale()
