from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsTextItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.toPlainText())})"
