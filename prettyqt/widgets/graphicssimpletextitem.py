from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsSimpleTextItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsSimpleTextItem(QtWidgets.QGraphicsSimpleTextItem):
    pass
