from __future__ import annotations

from collections.abc import Iterator
import ctypes
import math

from prettyqt import core, gui
from prettyqt.qt import API, QtCore, QtGui
from prettyqt.utils import types


class PolygonF(QtGui.QPolygonF):
    def __repr__(self):
        points_str = ", ".join([repr(i) for i in self])
        return f"{type(self).__name__}({points_str})"

    def __iter__(self) -> Iterator[core.PointF]:
        return iter(self.get_point(i) for i in range(self.size()))

    def __len__(self) -> int:
        return self.size()

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, point: types.PointFType) -> bool:
        if isinstance(point, tuple):
            point = core.PointF(*point)
        return self.containsPoint(point, QtCore.Qt.FillRule.OddEvenFill)

    def __getitem__(self, index: int) -> core.PointF:
        if index >= self.size():
            raise KeyError(index)
        return self.get_point(index)

    # def __setitem__(self, index: int, value: types.PointType):
    #     if isinstance(value, tuple):
    #         self.setPoint(index, *value)
    #     else:
    #         self.setPoint(index, value)

    def __sub__(self, other: QtGui.QPolygonF) -> PolygonF:
        return PolygonF(self.subtracted(other))

    def __and__(self, other: QtGui.QPolygonF) -> PolygonF:  # &
        return PolygonF(self.intersected(other))

    def __xor__(self, other: QtGui.QPolygonF) -> PolygonF:  # ^
        union = self | other
        intersect = self & other
        return union - intersect

    def __or__(self, other: QtGui.QPolygonF) -> PolygonF:  # |
        return PolygonF(self.united(other))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return list(self) == [other.at(i) for i in range(other.size())]

    def get_point(self, index: int) -> core.PointF:
        return core.PointF(self.at(index))

    def get_points(self) -> list[core.PointF]:
        return [self.get_point(i) for i in range(self.size())]

    def add_points(self, *points: types.PointFType):
        for p in points:
            if isinstance(p, tuple):
                p = core.PointF(*p)
            self.append(p)

    def to_polygon(self) -> gui.Polygon:
        return gui.Polygon(self.toPolygon())

    @classmethod
    def create_star(cls):
        poly = cls()
        poly.append(core.PointF(1.0, 0.5))
        for i in range(1, 5):
            val = 0.8 * i * math.pi
            point = core.PointF(0.5 + 0.5 * math.cos(val), 0.5 + 0.5 * math.sin(val))
            poly.append(point)
        return poly

    @classmethod
    def create_diamond(cls):
        points = [
            core.PointF(0.4, 0.5),
            core.PointF(0.5, 0.4),
            core.PointF(0.6, 0.5),
            core.PointF(0.5, 0.6),
            core.PointF(0.4, 0.5),
        ]
        poly = gui.PolygonF()
        poly.add_points(*points)
        return poly

    def get_data_buffer(self, size: int):
        self.resize(size)
        if API == "pyside6":
            import shiboken6

            address = shiboken6.getCppPointer(self.data())
            buffer = (ctypes.c_double * 2 * self.size()).from_address(address[0])
        elif API == "pyside2":
            import shiboken2

            address = shiboken2.getCppPointer(self.data())
            buffer = (ctypes.c_double * 2 * self.size()).from_address(address)
        else:
            buffer = self.data()
            buffer.setsize(16 * self.size())
        return buffer

    @classmethod
    def from_xy(cls, xdata, ydata) -> PolygonF:
        import numpy as np

        size = len(xdata)
        polyline = cls()
        buffer = polyline.get_data_buffer(size)
        memory = np.frombuffer(buffer, np.float64)
        memory[: (size - 1) * 2 + 1 : 2] = np.array(xdata, dtype=np.float64, copy=False)
        memory[1 : (size - 1) * 2 + 2 : 2] = np.array(ydata, dtype=np.float64, copy=False)
        return polyline


if __name__ == "__main__":
    poly = PolygonF([core.Point(1, 1), core.Point(2, 2)])
    poly2 = PolygonF([core.Point(1, 1), core.Point(2, 2)])
    new = poly | poly2
    print(repr(new))
