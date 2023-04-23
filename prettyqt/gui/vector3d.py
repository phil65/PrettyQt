from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


class Vector3D(QtGui.QVector3D):
    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return ba.data()

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector3D(0, 0, 1)
    print(abs(vector))
