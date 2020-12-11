from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QGraphicsObject.__bases__ = (core.Object, widgets.GraphicsItem)


class GraphicsObject(QtWidgets.QGraphicsObject):
    def serialize_fields(self):
        return dict(
            enabled=self.isEnabled(),
            opacity=self.opacity(),
            pos=core.PointF(self.pos()),
            # z=self.z(),
            rotation=self.rotation(),
            scale=self.scale(),
            transform_origin_point=core.PointF(self.transformOriginPoint()),
            visible=self.isVisible(),
            graphics_effect=self.graphicsEffect(),
        )
