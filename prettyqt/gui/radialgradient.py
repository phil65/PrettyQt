from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


QtGui.QRadialGradient.__bases__ = (gui.Gradient,)


class RadialGradient(QtGui.QRadialGradient):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.get_center()}, {self.centerRadius()}, "
            f"{self.get_focal_point()}, {self.focalRadius()})"
        )

    def serialize_fields(self):
        center = self.center()
        focal_point = self.focalPoint()
        return dict(
            center_radius=self.centerRadius(),
            radius=self.radius(),
            focal_radius=self.focalRadius(),
            center=(center[0], center[1]),
            focal_point=(focal_point[0], focal_point[1]),
        )

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_focal_point(self) -> core.PointF:
        return core.PointF(self.focalPoint())
