from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import types


class GraphicsScale(widgets.GraphicsTransformMixin, QtWidgets.QGraphicsScale):
    def set_origin(self, origin: types.VectorType):
        if not isinstance(origin, QtGui.QVector3D):
            origin = QtGui.QVector3D(*origin)
        self.setOrigin(origin)


if __name__ == "__main__":
    scale = GraphicsScale()
    scale.set_origin((1, 1, 1))
