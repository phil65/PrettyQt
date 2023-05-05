from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class PointF(QtCore.QPointF):
    def __repr__(self):
        return get_repr(self, self.x(), self.y())

    @property
    def _x(self):
        return self.x()

    @property
    def _y(self):
        return self.y()

    __match_args__ = ("_x", "_y")

    def __getitem__(self, index) -> float:
        match index:
            case 0:
                return self.x()
            case 1:
                return self.y()
            case _:
                raise IndexError(f"Invalid index {index} for Point")

    def __setitem__(self, i, x: float):
        match i:
            case 0:
                return self.setX(x)
            case 1:
                return self.setY(x)
            case _:
                raise IndexError(f"Invalid index {i} for Point")

    def __reduce__(self):
        return type(self), (self.x(), self.y())
