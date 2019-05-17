# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


class Validator(QtGui.QValidator):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __add__(self, other):
        if isinstance(other, Validator):
            from prettyqt import custom_validators
            return custom_validators.CompositeValidator([self, other])

    def __radd__(self, other):
        """
        needed for sum()
        """
        return self.__add__(other)

    def is_valid_value(self, value, pos=0) -> bool:
        val = self.validate(value, pos)
        return val[0] == self.Acceptable


Validator.__bases__[0].__bases__ = (core.Object,)


if __name__ == "__main__":
    val = Validator()
