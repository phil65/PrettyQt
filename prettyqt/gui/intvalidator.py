from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr

MAX_VAL = 2147483647


class IntValidator(gui.ValidatorMixin, QtGui.QIntValidator):
    ID = "integer_classic"

    def __repr__(self):
        return get_repr(self, self.bottom(), self.top())

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __reduce__(self):
        return type(self), (self.bottom(), self.top()), None

    def __eq__(self, other: object):
        return (
            self.bottom() == other.bottom() and self.top() == other.top()
            if isinstance(other, type(self))
            else False
        )

    def set_range(self, lower: int | None, upper: int | None):
        if lower is None:
            lower = -MAX_VAL
        if upper is None:
            upper = MAX_VAL
        self.setRange(lower, upper)


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
