# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class RegularExpression(QtCore.QRegularExpression):

    def __repr__(self):
        return f"RegularExpression({self.pattern()!r})"

    def __reduce__(self):
        return (self.__class__, (self.pattern(),))

    def matches_in_text(self, text):
        result = self.match(text)
        for i, hit in enumerate(result.capturedTexts()):
            yield result.capturedStart(i), result.capturedLength(i)


if __name__ == "__main__":
    reg = RegularExpression()
    reg.setPattern("[0-9]+ [a-z] [0-9]+")
    for i in reg.matches_in_text("033 a 03444"):
        print(i)
