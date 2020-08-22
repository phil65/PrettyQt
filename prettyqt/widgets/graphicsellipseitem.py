from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QGraphicsEllipseItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsEllipseItem(QtWidgets.QGraphicsEllipseItem):
    def serialize_fields(self):
        return dict(
            rect=core.RectF(self.rect()),
            span_angle=self.spanAngle(),
            start_angle=self.startAngle(),
        )
