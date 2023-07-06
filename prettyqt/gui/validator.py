from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class ValidatorMixin(core.ObjectMixin):
    def __repr__(self):
        return get_repr(self)

    def __and__(self, other: Validator):
        from prettyqt import validators

        return validators.AndValidator([self, other])

    def __or__(self, other: Validator):
        from prettyqt import validators

        return validators.OrValidator([self, other])

    def is_valid_value(self, value: str, pos: int = 0) -> bool:
        val = self.validate(value, pos)
        return val[0] == self.State.Acceptable  # type: ignore


class Validator(ValidatorMixin, QtGui.QValidator):
    pass


if __name__ == "__main__":
    val = Validator() & Validator()
    print(val)
