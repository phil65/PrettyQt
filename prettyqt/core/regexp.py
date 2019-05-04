# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class RegExp(QtCore.QRegExp):

    def __getstate__(self):
        return dict(regex=self.pattern())

    def __setstate__(self, state):
        super().__init__(state["regex"])

    def matches_in_text(self, text):
        index = self.indexIn(text)
        while index >= 0:
            length = self.matchedLength()
            yield index, length
            index = self.indexIn(text, index + length)
