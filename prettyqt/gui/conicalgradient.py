from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import get_repr


class ConicalGradient(gui.GradientMixin, gui.QConicalGradient):
    def __repr__(self):
        return get_repr(self, self.get_center(), self.angle())

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())
