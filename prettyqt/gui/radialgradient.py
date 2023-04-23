from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class RadialGradient(gui.GradientMixin, QtGui.QRadialGradient):
    def __repr__(self):
        return get_repr(
            self,
            self.get_center(),
            self.centerRadius(),
            self.get_focal_point(),
            self.focalRadius(),
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
