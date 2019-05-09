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
        super().__init__(state["bottom"], state["top"], state["decimals"])


if __name__ == "__main__":
    val = DoubleValidator()
    val.setRange(0, 9)
