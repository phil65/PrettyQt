from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsSimpleTextItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsSimpleTextItem(QtWidgets.QGraphicsSimpleTextItem):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.text()!r})"
