from typing import Self

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class Quaternion(QtGui.QQuaternion):
    """Represents a quaternion consisting of a vector and scalar."""

    def __repr__(self):
        return get_repr(self, self.scalar(), self.x(), self.y(), self.z())

    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    def __reduce__(self):
        return type(self), (self.scalar(), self.x(), self.y(), self.z())

    def get_vector(self) -> gui.Vector3D:
        return gui.Vector3D(self.vector())

    def to_euler_angles(self) -> gui.Vector3D:
        return gui.Vector3D(self.toEulerAngles())

    def to_vector4d(self) -> gui.Vector4D:
        return gui.Vector4D(self.toVector4D())

    def get_normalized(self) -> Self:
        return type(self)(self.normalized())

    def get_conjugated(self) -> Self:
        return type(self)(self.conjugated())

    def get_inverted(self) -> Self:
        return type(self)(self.inverted())


if __name__ == "__main__":
    quat = Quaternion(1, 0, 0, 0)
    print(repr(quat))
