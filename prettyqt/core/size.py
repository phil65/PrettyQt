from __future__ import annotations

from typing import Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class Size(QtCore.QSize):
    """Defines the size of a two-dimensional object using integer point precision."""

    def __repr__(self):
        return get_repr(self, self.width(), self.height())

    @property
    def _width(self) -> int:
        return self.width()

    @property
    def _height(self) -> int:
        return self.height()

    __match_args__ = ("_width", "_height")

    def __getitem__(self, index) -> int:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return type(self), (self.width(), self.height())

    def expanded_to(self, size: datatypes.SizeType) -> Self:
        size = datatypes.to_size(size)
        return type(self)(self.expandedTo(size))

    def shrunk_by(self, margins: datatypes.MarginsType) -> Self:
        margins = datatypes.to_margins(margins)
        return type(self)(self.shrunkBy(margins))

    def grown_by(self, margins: datatypes.MarginsType) -> Self:
        margins = datatypes.to_margins(margins)
        return type(self)(self.grownBy(margins))


if __name__ == "__main__":
    size = Size(10, 20)
    size = size.expanded_to(QtCore.QSize(100, 100))
