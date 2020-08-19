from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsPixmapItem.__bases__ = (widgets.GraphicsItem,)


class GraphicsPixmapItem(QtWidgets.QGraphicsPixmapItem):
    pass
