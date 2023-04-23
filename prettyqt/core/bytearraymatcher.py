from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class ByteArrayMatcher(QtCore.QByteArrayMatcher):
    def __repr__(self):
        return get_repr(self, self.get_pattern())

    def get_pattern(self) -> bytes:
        return bytes(self.pattern())


if __name__ == "__main__":
    matcher = ByteArrayMatcher(QtCore.QByteArray(b"Test"))
