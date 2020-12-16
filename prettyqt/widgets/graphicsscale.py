from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsScale.__bases__ = (widgets.GraphicsTransform,)


class GraphicsScale(QtWidgets.QGraphicsScale):
    pass


if __name__ == "__main__":
    transform = GraphicsScale()
