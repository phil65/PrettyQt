from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QGraphicsTransform.__bases__ = (core.Object,)


class GraphicsTransform(QtWidgets.QGraphicsTransform):
    pass


if __name__ == "__main__":
    transform = GraphicsTransform()
