# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class DirIterator(QtCore.QDirIterator):

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        raise StopIteration
