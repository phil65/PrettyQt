from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class PointF(QtCore.QPointF):
    def __repr__(self):
        return get_repr(self, x=self.x(), y=self.y())

    def __getitem__(self, index) -> float:
        return (self.x(), self.y())[index]

    def __reduce__(self):
        return type(self), (self.x(), self.y())
