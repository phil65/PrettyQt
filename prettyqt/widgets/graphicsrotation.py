from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, datatypes


class GraphicsRotation(widgets.GraphicsTransformMixin, QtWidgets.QGraphicsRotation):
    def set_axis(self, axis: constants.AxisStr):
        if axis not in constants.AXIS:
            raise InvalidParamError(axis, constants.AXIS)
        self.setAxis(constants.AXIS[axis])

    def set_origin(self, origin: datatypes.VectorType):
        if not isinstance(origin, QtGui.QVector3D):
            origin = QtGui.QVector3D(*origin)
        self.setOrigin(origin)


if __name__ == "__main__":
    rotation = GraphicsRotation()
    rotation.set_origin((1, 1, 1))
    print(rotation.origin())
