from __future__ import annotations

from typing_extensions import Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class Rect(QtCore.QRect):
    """Defines a rectangle in the plane using integer precision."""

    def __repr__(self):
        return get_repr(self, self.x(), self.y(), self.width(), self.height())

    @property
    def _x(self) -> int:
        return self.x()

    @property
    def _y(self) -> int:
        return self.y()

    @property
    def _width(self) -> int:
        return self.width()

    @property
    def _height(self) -> int:
        return self.height()

    __match_args__ = ("_x", "_y", "width", "height")

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.width(), self.height())

    def margins_added(self, margins: datatypes.MarginsType) -> Self:
        margins = datatypes.to_margins(margins)
        return type(self)(self.marginsAdded(margins))

    def margins_removed(self, margins: datatypes.MarginsType) -> Self:
        margins = datatypes.to_margins(margins)
        return type(self)(self.marginsRemoved(margins))


if __name__ == "__main__":
    rect = Rect(0, 2, 5, 5)
    print(repr(rect))
