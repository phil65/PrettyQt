from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class GraphicsScale(widgets.GraphicsTransformMixin, QtWidgets.QGraphicsScale):
    pass


if __name__ == "__main__":
    transform = GraphicsScale()
