from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class SizeF(QtCore.QSizeF):
    def __repr__(self):
        return get_repr(self, self.width(), self.height())

    @property
    def _width(self):
        return self.width()

    @property
    def _height(self):
        return self.height()

    __match_args__ = ("_width", "_height")

    def __getitem__(self, index) -> float:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return type(self), (self.width(), self.height())

    def expanded_to(self, size: datatypes.SizeFType) -> SizeF:
        if isinstance(size, tuple):
            size = QtCore.QSizeF(*size)
        return SizeF(self.expandedTo(size))

    def shrunk_by(self, margins: datatypes.MarginsFType) -> SizeF:
        if isinstance(margins, tuple):
            margins = QtCore.QMarginsF(*margins)
        return SizeF(self.marginsAdded(margins))

    def grown_by(self, margins: datatypes.MarginsFType) -> SizeF:
        if isinstance(margins, tuple):
            margins = QtCore.QMarginsF(*margins)
        return SizeF(self.marginsRemoved(margins))


if __name__ == "__main__":
    size = SizeF(10, 20)
    print(tuple(size))
    size = size.expanded_to(QtCore.QSizeF(100, 100))
    print(type(size))
