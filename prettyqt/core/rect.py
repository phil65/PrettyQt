from __future__ import annotations

from prettyqt.qt import QtCore


class Rect(QtCore.QRect):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.x()}, {self.y()}, "
            f"{self.width()}, {self.height()})"
        )

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.width(), self.height())


if __name__ == "__main__":
    rect = Rect(0, 2, 5, 5)
    print(repr(rect))
