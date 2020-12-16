from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QAbstractGraphicsShapeItem.__bases__ = (widgets.GraphicsItem,)


class AbstractGraphicsShapeItem(QtWidgets.QAbstractGraphicsShapeItem):
    def serialize_fields(self):
        return dict(brush=gui.Brush(self.brush()), pen=gui.Pen(self.pen()))
