from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


class Vector4D(QtGui.QVector4D):
    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    @property
    def _x(self):
        return self.x()

    @property
    def _y(self):
        return self.y()

    @property
    def _z(self):
        return self.z()

    @property
    def _w(self):
        return self.w()

    __match_args__ = ("_x", "_y", "z", "w")

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.z(), self.w())

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector4D(0, 0, 0, 1)
