from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class ConicalGradient(gui.GradientMixin, QtGui.QConicalGradient):
    def __repr__(self):
        return get_repr(self, self.get_center(), self.angle())

    def serialize_fields(self):
        center = self.center()
        return dict(angle=self.angle(), center=(center[0], center[1]))

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())
