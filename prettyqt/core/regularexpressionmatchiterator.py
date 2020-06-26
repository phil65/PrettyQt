# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class RegularExpressionMatchIterator(QtCore.QRegularExpressionMatchIterator):

    def __repr__(self):
        return "RegularExpressionMatchIterator()"

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        raise StopIteration


if __name__ == "__main__":
    reg = RegularExpressionMatchIterator()
