# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class DateTime(QtCore.QDateTime):

    def __repr__(self):
        return f"DateTime({self.date()}, {self.time()})"

    def __reduce__(self):
        return (self.__class__, (self.date(), self.time()))


if __name__ == "__main__":
    date = core.Date(2000, 11, 11)
    dt = DateTime(date)
