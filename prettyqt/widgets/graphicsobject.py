from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class GraphicsObjectMixin(core.ObjectMixin, widgets.GraphicsItemMixin):
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


class GraphicsObject(GraphicsObjectMixin, QtWidgets.QGraphicsObject):
    pass
