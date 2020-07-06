# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtGui

from prettyqt import core


QtGui.QValidator.__bases__ = (core.Object,)


class Validator(QtGui.QValidator):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __add__(self, other):
        if isinstance(other, Validator):
            from prettyqt import custom_validators

            return custom_validators.CompositeValidator([self, other])

    def __radd__(self, other: QtGui.QValidator):
        """
        needed for sum()
        """
        return self.__add__(other)

    def is_valid_value(self, value: str, pos: int = 0) -> bool:
        val = self.validate(value, pos)
        return val[0] == self.Acceptable


if __name__ == "__main__":
    val = Validator()
