from __future__ import annotations

from prettyqt.qt import QtCore


class ByteArray(QtCore.QByteArray):
    def __reduce__(self):
        return type(self), (bytes(self),)
