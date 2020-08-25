from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsItemGroup.__bases__ = (widgets.GraphicsItem,)


class GraphicsItemGroup(QtWidgets.QGraphicsItemGroup):
    pass
