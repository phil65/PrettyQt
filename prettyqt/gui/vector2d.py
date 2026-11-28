from prettyqt import core, gui
from prettyqt.qt import QtGui


class Vector2D(QtGui.QVector2D):
    """Represents a vector or vertex in 2D space."""

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

    __match_args__ = ("_x", "_y")

    def __reduce__(self):
        return type(self), (self.x(), self.y())

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())

    def to_vector3d(self) -> gui.Vector3D:
        return gui.Vector3D(self.toVector3D())

    def to_vector4d(self) -> gui.Vector4D:
        return gui.Vector4D(self.toVector4D())


if __name__ == "__main__":
    vector = Vector2D(3, 4)
    print(abs(vector))
