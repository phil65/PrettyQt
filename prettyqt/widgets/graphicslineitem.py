from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsLineItem.__bases__ = (widgets.GraphicsItem,)


class GraphicsLineItem(QtWidgets.QGraphicsLineItem):
    pass
