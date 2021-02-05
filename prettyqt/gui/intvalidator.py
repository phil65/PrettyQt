from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QIntValidator.__bases__ = (gui.Validator,)


class IntValidator(QtGui.QIntValidator):
    def __repr__(self):
        return f"{type(self).__name__}({self.bottom()}, {self.top()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __reduce__(self):
        return type(self), (self.bottom(), self.top()), None

    def __eq__(self, other: object):
        if not isinstance(other, type(self)):
            return False
        return self.bottom() == other.bottom() and self.top() == other.top()

    def set_range(self, lower: int | None, upper: int | None):
        if lower is None:
            lower = 2147483647  # number from docs
        if upper is None:
            upper = 2147483647
        self.setRange(lower, upper)


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
