from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QBuffer.__bases__ = (core.IODevice,)


class Buffer(QtCore.QBuffer):
    pass
