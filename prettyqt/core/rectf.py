from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class RectF(QtCore.QRectF):
    def __repr__(self):
        return get_repr(self, self.x(), self.y(), self.width(), self.height())

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.width(), self.height())


if __name__ == "__main__":
    rect = RectF(0, 2, 5, 5)
    print(repr(rect))
