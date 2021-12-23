from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import types


class SizeF(QtCore.QSizeF):
    def __repr__(self):
        return f"{type(self).__name__}({self.width()}, {self.height()})"

    def __getitem__(self, index) -> float:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return type(self), (self.width(), self.height())

    def expanded_to(self, size: types.SizeFType) -> SizeF:
        if isinstance(size, tuple):
            size = QtCore.QSizeF(*size)
        return SizeF(self.expandedTo(size))

    def shrunk_by(self, margins: types.MarginsFType) -> SizeF:
        if isinstance(margins, tuple):
            margins = QtCore.QMarginsF(*margins)
        return SizeF(self.marginsAdded(margins))

    def grown_by(self, margins: types.MarginsFType) -> SizeF:
        if isinstance(margins, tuple):
            margins = QtCore.QMarginsF(*margins)
        return SizeF(self.marginsRemoved(margins))


if __name__ == "__main__":
    size = SizeF(10, 20)
    print(tuple(size))
    size = size.expanded_to(QtCore.QSizeF(100, 100))
    print(type(size))
