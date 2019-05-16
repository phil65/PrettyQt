# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class IntValidator(QtGui.QIntValidator):

    def __repr__(self):
        return f"IntValidator({self.bottom()}, {self.top()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __setstate__(self, state):
        self.__init__(state["bottom"], state["top"])


IntValidator.__bases__[0].__bases__ = (gui.Validator,)


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
