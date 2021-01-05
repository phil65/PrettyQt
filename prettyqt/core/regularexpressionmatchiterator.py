from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class RegularExpressionMatchIterator(QtCore.QRegularExpressionMatchIterator):
    def __repr__(self):
        return f"{type(self).__name__}()"

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
