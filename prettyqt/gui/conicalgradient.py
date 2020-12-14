from qtpy import QtGui

from prettyqt import gui, core


QtGui.QConicalGradient.__bases__ = (gui.Gradient,)


class ConicalGradient(QtGui.QConicalGradient):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_center()}, {self.angle()})"

    def serialize_fields(self):
        center = self.center()
        return dict(angle=self.angle(), center=(center[0], center[1]))

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())
