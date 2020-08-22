from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsPathItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsPathItem(QtWidgets.QGraphicsPathItem):
    pass
