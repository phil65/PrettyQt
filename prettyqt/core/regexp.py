# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class RegExp(QtCore.QRegExp):

    def matches_in_text(self, text):
        index = self.indexIn(text)
        while index >= 0:
            length = self.matchedLength()
            yield index, length
            index = self.indexIn(text, index + length)
