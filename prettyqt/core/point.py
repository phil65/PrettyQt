from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class Point(QtCore.QPoint):
    """Defines a point in the plane using integer precision."""

    def __repr__(self):
        return get_repr(self, self.x(), self.y())

    @property
    def _x(self) -> int:
        return self.x()

    @property
    def _y(self) -> int:
        return self.y()

    __match_args__ = ("_x", "_y")

    def __getitem__(self, index) -> int:
        match index:
            case 0:
                return self.x()
            case 1:
                return self.y()
            case _:
                raise IndexError(f"Invalid index {index} for Point")

    def __setitem__(self, i, x: int):
        match i:
            case 0:
                return self.setX(x)
            case 1:
                return self.setY(x)
            case _:
                raise IndexError(f"Invalid index {i} for Point")

    def __reduce__(self):
        return type(self), (self.x(), self.y())


if __name__ == "__main__":
    p = Point(0, 1)
    match p:
        case Point(0, 1):
            raise Exception("yeah")
