# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class DoubleValidator(QtGui.QDoubleValidator):

    def __repr__(self):
        return f"DoubleValidator({self.bottom()}, {self.top()}, {self.decimals()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top(), decimals=self.decimals())

    def __setstate__(self, state):
        self.__init__(state["bottom"], state["top"], state["decimals"])

    def is_valid_value(self, value) -> bool:
        val = self.validate(value, 0)
        return val[0] == self.Acceptable


if __name__ == "__main__":
    val = DoubleValidator()
    val.setRange(0, 9)
