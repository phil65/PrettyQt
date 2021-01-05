from __future__ import annotations

from typing import Optional

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QDoubleValidator.__bases__ = (gui.Validator,)


class DoubleValidator(QtGui.QDoubleValidator):
    def __repr__(self):
        return f"{type(self).__name__}({self.bottom()}, {self.top()}, {self.decimals()})"

    def __reduce__(self):
        return type(self), (self.bottom(), self.top(), self.decimals()), None

    def __eq__(self, other: object):
        if not isinstance(other, type(self)):
            return False
        return (
            self.bottom() == other.bottom()
            and self.top() == other.top()
            and self.decimals() == other.decimals()
        )

    def serialize_fields(self):
        return dict(bottom=self.bottom(), top=self.top(), decimals=self.decimals())

    def set_range(self, start: Optional[float], end: Optional[float], decimals: int = 0):
        if start is None:
            start = -float("inf")
        if end is None:
            end = float("inf")
        self.setRange(start, end, decimals)


if __name__ == "__main__":
    val = DoubleValidator()
    val.setRange(0, 9)
