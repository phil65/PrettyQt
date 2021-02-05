from __future__ import annotations

from prettyqt.qt import QtCore


class Size(QtCore.QSize):
    def __repr__(self):
        return f"{type(self).__name__}({self.width()}, {self.height()})"

    def __getitem__(self, index) -> int:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return type(self), (self.width(), self.height())

    def expanded_to(self, size: QtCore.QSize | tuple[int, int]) -> Size:
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        return Size(self.expandedTo(size))


if __name__ == "__main__":
    size = Size(10, 20)
    print(tuple(size))
    size = size.expanded_to(QtCore.QSize(100, 100))
    print(type(size))
