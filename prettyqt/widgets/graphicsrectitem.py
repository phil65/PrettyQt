from qtpy import QtWidgets

from prettyqt import widgets, core


QtWidgets.QGraphicsRectItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def get_rect(self):
        return core.RectF(self.rect())

    def serialize_fields(self):
        return dict(rect=self.get_rect())
