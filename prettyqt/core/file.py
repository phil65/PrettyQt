from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QFile.__bases__ = (core.FileDevice,)


class File(QtCore.QFile):
    pass
