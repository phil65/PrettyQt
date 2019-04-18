# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtGui


class RegExpValidator(QtGui.QRegExpValidator):

    def set_regex(self, regex):
        re = QtCore.QRegExp(regex)
        self.setRegExp(re)


if __name__ == "__main__":
    val = RegExpValidator()
    val.set_regex(r"\w\d\d")
