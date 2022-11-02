from __future__ import annotations

from collections.abc import Iterator
import ctypes

from prettyqt import core
from prettyqt.qt import API, QtCore, QtGui
from prettyqt.utils import types


class Polygon(QtGui.QPolygon):
    def __repr__(self):
        points_str = ", ".join([repr(i) for i in self])
        return f"{type(self).__name__}({points_str})"

    def __iter__(self) -> Iterator[core.Point]:
        return iter(self.get_point(i) for i in range(self.size()))

    def __len__(self) -> int:
        return self.size()

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, point: types.PointType) -> bool:
        if isinstance(point, tuple):
            point = core.Point(*point)
        return self.containsPoint(point, QtCore.Qt.FillRule.OddEvenFill)

    def __getitem__(self, index: int) -> core.Point:
        if index >= self.size():
            raise KeyError(index)
        return self.get_point(index)

    def __setitem__(self, index: int, value: types.PointType):
        if isinstance(value, tuple):
            p = core.Point(*value)
        else:
            p = value
        # PySide2 workaround: setPoint does not exist
        self.remove(index)
        self.insert(index, p)

    def __sub__(self, other: QtGui.QPolygon) -> Polygon:
        return Polygon(self.subtracted(other))

    def __and__(self, other: QtGui.QPolygon) -> Polygon:  # &
        return Polygon(self.intersected(other))

    def __xor__(self, other: QtGui.QPolygon) -> Polygon:  # ^
        union = self | other
        intersect = self & other
        return union - intersect

    def __or__(self, other: QtGui.QPolygon) -> Polygon:  # |
        return Polygon(self.united(other))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def get_point(self, index: int) -> core.Point:
        # PySide2 doesnt have self.point method
        return core.Point(self.value(index))

    def get_points(self) -> list[core.Point]:
        return [self.get_point(i) for i in range(self.size())]

    def add_points(self, *points: types.PointType):
        for p in points:
            if isinstance(p, tuple):
                p = core.Point(*p)
            self.append(p)

    def get_data_buffer(self, size: int):
        self.resize(size)
        if API == "pyside6":
            import shiboken6

            address = shiboken6.getCppPointer(self.data())
            buffer = (ctypes.c_long * 2 * self.size()).from_address(address[0])
        elif API == "pyside2":
            import shiboken2

            address = shiboken2.getCppPointer(self.data())
            buffer = (ctypes.c_long * 2 * self.size()).from_address(address)
        else:
            buffer = self.data()
            buffer.setsize(8 * self.size())
        return buffer

    @classmethod
    def from_xy(cls, xdata, ydata) -> Polygon:
        import numpy as np

        size = len(xdata)
        polyline = cls()
        buffer = polyline.get_data_buffer(size)
        memory = np.frombuffer(buffer, np.float64)
        memory[: (size - 1) * 2 + 1 : 2] = np.array(xdata, dtype=np.float64, copy=False)
        memory[1 : (size - 1) * 2 + 2 : 2] = np.array(ydata, dtype=np.float64, copy=False)
        return polyline


if __name__ == "__main__":
    poly = Polygon([core.Point(1, 1), core.Point(2, 2)])
    poly2 = Polygon([core.Point(1, 1), core.Point(2, 2)])
    poly.get_data_buffer(10)
    poly & poly2
