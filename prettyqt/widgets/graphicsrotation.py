from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QGraphicsRotation.__bases__ = (widgets.GraphicsTransform,)


class GraphicsRotation(QtWidgets.QGraphicsRotation):
    def set_axis(self, axis: constants.AxisStr):
        if axis not in constants.AXIS:
            raise InvalidParamError(axis, constants.AXIS)
        self.setAxis(constants.AXIS[axis])


if __name__ == "__main__":
    transform = GraphicsRotation()
