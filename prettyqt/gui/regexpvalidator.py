# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core, gui


QtGui.QRegExpValidator.__bases__ = (gui.Validator,)


class RegExpValidator(QtGui.QRegExpValidator):

    def __repr__(self):
        return f"RegExpValidator(RegExp({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(regexp=core.RegExp(self.regExp()))

    def __setstate__(self, state):
        self.__init__()
        self.setRegExp(state["regexp"])

    def set_regex(self, regex: str):
        re = core.RegExp(regex)
        self.setRegExp(re)

    def get_regex(self) -> str:
        val = self.regExp()
        return val.pattern()


if __name__ == "__main__":
    val = RegExpValidator()
    val.set_regex(r"\w\d\d")
