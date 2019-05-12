# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class Validator(QtGui.QValidator):

    def __add__(self, other):
        if isinstance(other, Validator):
            from prettyqt import custom_validators
            return custom_validators.CompositeValidator([self, other])

    def __radd__(self, other):
        """
        needed for sum()
        """
        return self.__add__(other)

    def is_valid_value(self, value) -> bool:
        val = self.validate(value)
        return val[0] == self.Acceptable


if __name__ == "__main__":
    val = Validator()
