from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import serializemixin


class Vector3D(serializemixin.SerializeMixin, QtGui.QVector3D):
    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector3D(0, 0, 1)
    print(abs(vector))
