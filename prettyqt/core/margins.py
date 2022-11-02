from __future__ import annotations

from collections.abc import Iterator

from prettyqt.qt import QtCore


class Margins(QtCore.QMargins):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.left()}, {self.top()}, "
            f"{self.right()}, {self.bottom()})"
        )

    def __reduce__(self):
        return type(self), (self.left(), self.top(), self.right(), self.bottom())

    def __bool__(self):
        return not self.isNull()

    def __iter__(self) -> Iterator[int]:
        yield self.left()
        yield self.top()
        yield self.right()
        yield self.bottom()


if __name__ == "__main__":
    margins = Margins(0, 0, 0, 0)
    print(bool(margins))
