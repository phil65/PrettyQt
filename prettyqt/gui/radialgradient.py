from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import get_repr


class RadialGradient(gui.GradientMixin, gui.QRadialGradient):
    def __repr__(self):
        return get_repr(
            self,
            self.get_center(),
            self.centerRadius(),
            self.get_focal_point(),
            self.focalRadius(),
        )

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_focal_point(self) -> core.PointF:
        return core.PointF(self.focalPoint())


if __name__ == "__main__":
    grad = RadialGradient()
