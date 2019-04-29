# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class PolygonF(QtGui.QPolygonF):

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
