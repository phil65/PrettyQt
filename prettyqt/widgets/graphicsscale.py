from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import datatypes


class GraphicsScale(widgets.GraphicsTransformMixin, widgets.QGraphicsScale):
    def set_origin(self, origin: datatypes.Vector3DType):
        self.setOrigin(datatypes.to_vector3d(origin))


if __name__ == "__main__":
    scale = GraphicsScale()
    scale.set_origin((1, 1, 1))
