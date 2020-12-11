from qtpy import QtWidgets, QtCore

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError


AXIS = bidict(x=QtCore.Qt.XAxis, y=QtCore.Qt.YAxis, z=QtCore.Qt.ZAxis)

QtWidgets.QGraphicsRotation.__bases__ = (widgets.GraphicsTransform,)


class GraphicsRotation(QtWidgets.QGraphicsRotation):
    def set_axis(self, axis: str):
        if axis not in AXIS:
            raise InvalidParamError(axis, AXIS)
        self.setAxis(AXIS[axis])


if __name__ == "__main__":
    transform = GraphicsRotation()
