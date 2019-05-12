# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class IntValidator(QtGui.QIntValidator):

    def __repr__(self):
        return f"IntValidator({self.bottom()}, {self.top()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __setstate__(self, state):
        self.__init__(state["bottom"], state["top"])

    def is_valid_value(self, value) -> bool:
        val = self.validate(value, 0)
        return val[0] == self.Acceptable


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
