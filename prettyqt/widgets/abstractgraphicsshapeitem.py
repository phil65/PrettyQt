from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QAbstractGraphicsShapeItem.__bases__ = (widgets.GraphicsItem,)


class AbstractGraphicsShapeItem(QtWidgets.QAbstractGraphicsShapeItem):
    pass
