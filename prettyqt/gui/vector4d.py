from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


class Vector4D(QtGui.QVector4D):
    # def __repr__(self):
    #     return f"{type(self).__name__}()"
    pass

    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector4D(0, 0, 0, 1)
    print(abs(vector))
