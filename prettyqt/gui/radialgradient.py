from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


class RadialGradient(gui.GradientMixin, QtGui.QRadialGradient):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.get_center()}, {self.centerRadius()}, "
            f"{self.get_focal_point()}, {self.focalRadius()})"
        )

    def serialize_fields(self):
        return dict(
            center_radius=self.centerRadius(),
            radius=self.radius(),
            focal_radius=self.focalRadius(),
            center=self.center(),
            focal_point=self.focalPoint(),
        )

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_focal_point(self) -> core.PointF:
        return core.PointF(self.focalPoint())


if __name__ == "__main__":
    grad = RadialGradient()
    print(grad.serialize_fields())
