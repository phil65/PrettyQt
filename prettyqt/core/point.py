from __future__ import annotations

from prettyqt.qt import QtCore


class Point(QtCore.QPoint):
    def __repr__(self):
        return f"{type(self).__name__}(x={self.x()}, y={self.y()})"

    def __getitem__(self, index) -> int:
        return (self.x(), self.y())[index]

    def __reduce__(self):
        return type(self), (self.x(), self.y())
