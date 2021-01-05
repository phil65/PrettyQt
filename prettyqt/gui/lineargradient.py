from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


QtGui.QLinearGradient.__bases__ = (gui.Gradient,)


class LinearGradient(QtGui.QLinearGradient):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_start()}, {self.get_final_stop()})"

    def serialize_fields(self):
        start = self.start()
        final_stop = self.finalStop()
        return dict(start=(start[0], start[1]), final_stop=(final_stop[0], final_stop[1]))

    def get_start(self) -> core.PointF:
        return core.PointF(self.start())

    def get_final_stop(self) -> core.PointF:
        return core.PointF(self.finalStop())
