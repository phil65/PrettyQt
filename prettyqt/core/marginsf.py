from __future__ import annotations

from collections.abc import Iterator

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class MarginsF(QtCore.QMarginsF):
    def __repr__(self):
        return get_repr(self, self.left(), self.top(), self.right(), self.bottom())

    def __reduce__(self):
        return type(self), (self.left(), self.top(), self.right(), self.bottom())

    def __bool__(self):
        return not self.isNull()

    def __iter__(self) -> Iterator[float]:
        yield self.left()
        yield self.top()
        yield self.right()
        yield self.bottom()


if __name__ == "__main__":
    margins = MarginsF(0, 0, 0, 0)
    print(repr(margins))
