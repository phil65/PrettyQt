from __future__ import annotations

from collections.abc import Iterator
import ctypes

from typing_extensions import Self

from prettyqt import core, constants
from prettyqt.qt import API, QtGui
from prettyqt.utils import datatypes, serializemixin


class Polygon(serializemixin.SerializeMixin, QtGui.QPolygon):
    def __repr__(self):
        return f"{type(self).__name__}(<{len(self)} points>)"

    def __iter__(self) -> Iterator[core.Point]:
        return iter(self.get_point(i) for i in range(self.size()))

    def __len__(self) -> int:
        return self.size()

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, point: datatypes.PointType) -> bool:
        if isinstance(point, tuple):
            point = core.Point(*point)
        return self.containsPoint(point, constants.FillRule.OddEvenFill)

    def __getitem__(self, index: int) -> core.Point:
        if index >= self.size():
            raise KeyError(index)
        return self.get_point(index)

    def __setitem__(self, index: int, value: datatypes.PointType):
        p = core.Point(*value) if isinstance(value, tuple) else value
        # PySide6 workaround: setPoint does not exist
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

    def get_point(self, index: int) -> core.Point:
        # PySide6 doesnt have self.point method
        return core.Point(self.value(index))

    def get_points(self) -> list[core.Point]:
        return [self.get_point(i) for i in range(self.size())]

    def add_points(self, *points: datatypes.PointType):
        for p in points:
            point = core.Point(*p) if isinstance(p, tuple) else p
            self.append(point)

    def get_data_buffer(self, size: int):
        self.resize(size)
        if API == "pyside6":
            import shiboken6

            address = shiboken6.getCppPointer(self.data())
            buffer = (ctypes.c_long * 2 * self.size()).from_address(address[0])
        else:
            buffer = self.data()
            buffer.setsize(8 * self.size())
        return buffer

    @classmethod
    def from_xy(cls, xdata, ydata) -> Self:
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
