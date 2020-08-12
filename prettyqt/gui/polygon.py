# -*- coding: utf-8 -*-

from typing import Union, Tuple

from qtpy import QtGui

from prettyqt import core


class Polygon(QtGui.QPolygon):
    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def add_points(self, *points: Union[Tuple[float, float], core.Point]):
        for p in points:
            if isinstance(p, tuple):
                p = core.Point(*p)
            self << p

    @classmethod
    def from_xy(cls, xdata, ydata):
        import numpy as np

        size = len(xdata)
        polyline = cls(size)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)
        memory = np.frombuffer(pointer, dtype)
        memory[: (size - 1) * 2 + 1 : 2] = xdata
        memory[1 : (size - 1) * 2 + 2 : 2] = ydata
        return polyline


if __name__ == "__main__":
    poly = Polygon((core.Point(1, 1), core.Point(2, 2)))
