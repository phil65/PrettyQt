from qtpy import QtWidgets

from prettyqt import widgets, gui


QtWidgets.QAbstractGraphicsShapeItem.__bases__ = (widgets.GraphicsItem,)


class AbstractGraphicsShapeItem(QtWidgets.QAbstractGraphicsShapeItem):
    def serialize_fields(self):
        return dict(brush=gui.Brush(self.brush()), pen=gui.pen(self.pen()))
