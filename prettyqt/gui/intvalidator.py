from __future__ import annotations

from qtpy import QtGui

from prettyqt import gui


QtGui.QIntValidator.__bases__ = (gui.Validator,)


class IntValidator(QtGui.QIntValidator):
    def __repr__(self):
        return f"{type(self).__name__}({self.bottom()}, {self.top()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __reduce__(self):
        return type(self), (self.bottom(), self.top()), None

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return False
        return self.bottom() == other.bottom() and self.top() == other.top()


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
