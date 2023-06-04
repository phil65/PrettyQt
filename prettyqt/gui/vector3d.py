from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


class Vector3D(QtGui.QVector3D):
    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    @property
    def _x(self) -> float:
        return self.x()

    @property
    def _y(self) -> float:
        return self.y()

    @property
    def _z(self) -> float:
        return self.z()

    __match_args__ = ("_x", "_y", "z")

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.z())

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector3D(0, 0, 1)
    print(abs(vector))
