from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsTextItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    pass
