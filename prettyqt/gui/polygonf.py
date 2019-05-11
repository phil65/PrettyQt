# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtGui

from prettyqt import core


class PolygonF(QtGui.QPolygonF):

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.WriteOnly)
        stream << self
        return ba

    def __setstate__(self, ba):
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.ReadOnly)
        stream >> self

    @classmethod
    def from_xy(cls, xdata, ydata):
        import numpy as np
        size = len(xdata)
        polyline = cls(size)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)
        memory = np.frombuffer(pointer, dtype)
        memory[:(size - 1) * 2 + 1:2] = xdata
        memory[1:(size - 1) * 2 + 2:2] = ydata
        return polyline


if __name__ == "__main__":
    poly = PolygonF((core.Point(1, 1), core.Point(2, 2)))
