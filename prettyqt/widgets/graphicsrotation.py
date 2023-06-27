from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes


class GraphicsRotation(widgets.GraphicsTransformMixin, widgets.QGraphicsRotation):
    def set_axis(self, axis: constants.AxisStr | constants.Axis):
        self.setAxis(constants.AXIS.get_enum_value(axis))

    def set_origin(self, origin: datatypes.VectorType):
        if not isinstance(origin, QtGui.QVector3D):
            origin = QtGui.QVector3D(*origin)
        self.setOrigin(origin)


if __name__ == "__main__":
    rotation = GraphicsRotation()
    rotation.set_origin((1, 1, 1))
