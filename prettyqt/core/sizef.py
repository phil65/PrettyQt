from __future__ import annotations

from qtpy import QtCore


class SizeF(QtCore.QSizeF):
    def __repr__(self):
        return f"{type(self).__name__}({self.width()}, {self.height()})"

    def __getitem__(self, index) -> float:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return self.__class__, (self.width(), self.height())

    def expanded_to(self, size: QtCore.QSizeF) -> SizeF:
        return SizeF(self.expandedTo(size))


if __name__ == "__main__":
    size = SizeF(10, 20)
    print(tuple(size))
    size = size.expanded_to(QtCore.QSizeF(100, 100))
    print(type(size))
