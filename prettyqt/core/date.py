# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class Date(QtCore.QDate):

    def __reduce__(self):
        return (self.__class__, (self.year(), self.month(), self.day()))


if __name__ == "__main__":
    dt = Date(2000, 11, 11)
    print(dt)
