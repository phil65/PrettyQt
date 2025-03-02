from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self

from prettyqt import core
from prettyqt.utils import datatypes, get_repr


if TYPE_CHECKING:
    from collections.abc import Iterator


class LineF(core.QLineF):
    """Two-dimensional vector using floating point precision."""

    def __repr__(self):
        return get_repr(self, self.get_p1(), self.get_p2())

    @property
    def _x1(self) -> float:
        return self.get_x1()

    @property
    def _y1(self) -> float:
        return self.y1()

    @property
    def _x2(self) -> float:
        return self.x2()

    @property
    def _y2(self) -> float:
        return self.y2()

    __match_args__ = ("_x1", "_y1", "_x2", "_y2")

    def __reduce__(self):
        return type(self), (self.get_p1(), self.get_p1())

    def __reversed__(self):
        return LineF(self.get_p2(), self.get_p1())

    def __abs__(self) -> float:
        return self.length()

    def __iter__(self) -> Iterator[core.PointF]:
        yield self.get_p1()
        yield self.get_p2()

    def __getitem__(self, index: Literal[0, 1]) -> core.PointF:
        match index:
            case 0:
                return self.get_p1()
            case 1:
                return self.get_p2()
            case _:
                raise KeyError(index)

    def __setitem__(self, index: Literal[0, 1], value: datatypes.PointFType):
        match index:
            case 0:
                self.set_p1(value)
            case 1:
                self.set_p2(value)
            case _:
                raise KeyError(index)

    def set_p1(self, point: datatypes.PointFType):
        self.setP1(datatypes.to_pointf(point))

    def get_p1(self) -> core.PointF:
        return core.PointF(self.p1())

    def set_p2(self, point: datatypes.PointFType):
        self.setP2(datatypes.to_pointf(point))

    def get_p2(self) -> core.PointF:
        return core.PointF(self.p2())

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_normal_vector(self) -> Self:
        return type(self)(self.normalVector())

    def get_unit_vector(self) -> Self:
        return type(self)(self.unitVector())

    def to_line(self) -> core.Line:
        return core.Line(self.toLine())


if __name__ == "__main__":
    line = LineF(core.Point(0, 0), core.Point(2, 2))
