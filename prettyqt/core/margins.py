from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from collections.abc import Iterator


class Margins(QtCore.QMargins):
    """Defines the four margins of a rectangle."""

    def __repr__(self):
        return get_repr(self, self.left(), self.top(), self.right(), self.bottom())

    def __reduce__(self):
        return type(self), (self.left(), self.top(), self.right(), self.bottom())

    @property
    def _left(self) -> int:
        return self.left()

    @property
    def _top(self) -> int:
        return self.top()

    @property
    def _right(self) -> int:
        return self.right()

    @property
    def _bottom(self) -> int:
        return self.bottom()

    __match_args__ = ("_left", "_top", "_right", "_bottom")

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
