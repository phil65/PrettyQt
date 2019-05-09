# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui
from prettyqt import core


class RegExpValidator(QtGui.QRegExpValidator):

    def __repr__(self):
        return f"RegExpValidator(RegExp('{self.get_regex()}'))"

    def __getstate__(self):
        return dict(regexp=core.RegExp(self.regExp()))

    def __setstate__(self, state):
        super().__init__()
        self.setRegExp(state["regexp"])

    def set_regex(self, regex):
        re = core.RegExp(regex)
        self.setRegExp(re)

    def get_regex(self):
        val = self.regExp()
        return val.pattern()


if __name__ == "__main__":
    val = RegExpValidator()
    val.set_regex(r"\w\d\d")
