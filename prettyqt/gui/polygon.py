# -*- coding: utf-8 -*-

from typing import Union, Tuple, List

from qtpy import QtGui, QtCore

from prettyqt import core


class Polygon(QtGui.QPolygon):
    def __repr__(self):
        points_str = ", ".join([repr(i) for i in self])
        return f"Polygon({points_str})"

    def __iter__(self):
        return iter(self[i] for i in range(self.size()))

    def __len__(self) -> int:
        return self.size()

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, point: QtCore.QPoint) -> bool:
        return self.containsPoint(point, QtCore.Qt.OddEvenFill)

    def __getitem__(self, index: int) -> core.Point:
        return core.Point(self.point(index))

    def __setitem__(self, index: int, value: Union[QtCore.QPoint, Tuple[int, int]]):
        if isinstance(value, tuple):
            self.setPoint(index, *value)
        else:
            self.setPoint(index, value)

    def __sub__(self, other: QtGui.QPolygon) -> "Polygon":
        return Polygon(self.subtracted(other))

    def __and__(self, other: QtGui.QPolygon) -> "Polygon":  # &
        return Polygon(self.intersected(other))

    def __xor__(self, other: QtGui.QPolygon) -> "Polygon":  # ^
        union = self | other
        intersect = self & other
        return union - intersect

    def __or__(self, other: QtGui.QPolygon) -> "Polygon":  # |
        return Polygon(self.united(other))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def get_point(self, index: int) -> core.Point:
        return core.Point(self.point(index))

    def get_points(self) -> List[core.Point]:
        return [self.get_point(i) for i in range(len(self))]

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
    poly2 = Polygon((core.Point(1, 1), core.Point(2, 2)))
    poly & poly2
