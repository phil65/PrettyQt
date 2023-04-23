from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class RegularExpressionMatchIterator(QtCore.QRegularExpressionMatchIterator):
    def __repr__(self):
        return get_repr(self)

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return core.RegularExpressionMatch(self.next())
        raise StopIteration

    def peek_next(self) -> core.RegularExpressionMatch:
        return core.RegularExpressionMatch(self.peekNext())


if __name__ == "__main__":
    reg = RegularExpressionMatchIterator()
