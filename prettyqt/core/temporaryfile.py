from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QTemporaryFile.__bases__ = (core.File,)


class TemporaryFile(QtCore.QTemporaryFile):
    pass
