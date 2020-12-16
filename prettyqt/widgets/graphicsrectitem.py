from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QGraphicsRectItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.get_rect())})"

    def get_rect(self):
        return core.RectF(self.rect())

    def serialize_fields(self):
        return dict(rect=self.get_rect())
