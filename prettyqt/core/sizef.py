from __future__ import annotations

from typing_extensions import Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class SizeF(QtCore.QSizeF):
    """Defines the size of a two-dimensional object using floating point precision."""

    def __repr__(self):
        return get_repr(self, self.width(), self.height())

    @property
    def _width(self) -> float:
        return self.width()

    @property
    def _height(self) -> float:
        return self.height()

    __match_args__ = ("_width", "_height")

    def __getitem__(self, index) -> float:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return type(self), (self.width(), self.height())

    def expanded_to(self, size: datatypes.SizeFType) -> Self:
        size = datatypes.to_sizef(size)
        return type(self)(self.expandedTo(size))

    def shrunk_by(self, margins: datatypes.MarginsFType) -> Self:
        margins = datatypes.to_marginsf(margins)
        return type(self)(self.shrunkBy(margins))

    def grown_by(self, margins: datatypes.MarginsFType) -> Self:
        margins = datatypes.to_marginsf(margins)
        return type(self)(self.grownBy(margins))


if __name__ == "__main__":
    size = SizeF(10, 20)
