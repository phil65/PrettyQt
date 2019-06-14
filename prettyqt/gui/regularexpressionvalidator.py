# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core, gui


QtGui.QRegularExpressionValidator.__bases__ = (gui.Validator,)


class RegularExpressionValidator(QtGui.QRegularExpressionValidator):

    def __repr__(self):
        return f"RegularExpressionValidator(RegularExpression({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(regexp=core.RegularExpression(self.regularExpression()))

    def __setstate__(self, state):
        self.__init__()
        self.setRegularExpression(state["regexp"])

    def set_regex(self, regex: str):
        re = core.RegularExpression(regex)
        self.setRegularExpression(re)

    def get_regex(self) -> str:
        val = self.regularExpression()
        return val.pattern()


if __name__ == "__main__":
    val = RegularExpressionValidator()
    val.set_regex(r"\w\d\d")
