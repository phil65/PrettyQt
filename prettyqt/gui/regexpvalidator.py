# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore


class RegExpValidator(QtGui.QRegExpValidator):

    def set_regex(self, regex):
        re = QtCore.QRegExp(regex)
        self.setRegExp(re)
