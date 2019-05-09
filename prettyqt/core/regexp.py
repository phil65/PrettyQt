# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class RegExp(QtCore.QRegExp):

    def __repr__(self):
        return f"RegExp('{self.pattern()}')"

    def __reduce__(self):
        return (self.__class__, (self.pattern(),))

    def matches_in_text(self, text):
        index = self.indexIn(text)
        while index >= 0:
            length = self.matchedLength()
            yield index, length
            index = self.indexIn(text, index + length)


if __name__ == "__main__":
    reg = RegExp()
    reg.setPattern("[0-9]")
