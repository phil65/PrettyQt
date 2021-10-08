from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


QtGui.QValidator.__bases__ = (core.Object,)


class Validator(QtGui.QValidator):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __add__(self, other: Validator):
        from prettyqt import custom_validators

        return custom_validators.CompositeValidator([self, other])

    def __radd__(self, other: QtGui.QValidator):
        """Needed for sum()."""
        return self.__add__(other)

    def is_valid_value(self, value: str, pos: int = 0) -> bool:
        val = self.validate(value, pos)
        return val[0] == self.State.Acceptable  # type: ignore


if __name__ == "__main__":
    val = Validator()
