from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class RectF(QtCore.QRectF):
    def __repr__(self):
        return get_repr(self, self.x(), self.y(), self.width(), self.height())

    @property
    def _x(self):
        return self.x()

    @property
    def _y(self):
        return self.y()

    @property
    def _width(self):
        return self.width()

    @property
    def _height(self):
        return self.height()

    __match_args__ = ("_x", "_y", "width", "height")

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.width(), self.height())


if __name__ == "__main__":
    rect = RectF(0, 2, 5, 5)
    print(repr(rect))
