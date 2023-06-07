from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class LinearGradient(gui.GradientMixin, QtGui.QLinearGradient):
    def __repr__(self):
        return get_repr(self, self.get_start(), self.get_final_stop())

    def get_start(self) -> core.PointF:
        return core.PointF(self.start())

    def get_final_stop(self) -> core.PointF:
        return core.PointF(self.finalStop())

    def get_css_gradient(self) -> str:
        stop, finalStop = self.start(), self.finalStop()
        x1, y1, x2, y2 = stop.x(), stop.y(), finalStop.x(), finalStop.y()
        stops = self.stops()
        stops = "\n".join(f"    stop: {stop:f} {color.name()}" for stop, color in stops)
        return (
            "qlineargradient(\n"
            f"    x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},\n"
            f"{stops})"
        )
