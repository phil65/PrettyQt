from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QSaveFile.__bases__ = (core.FileDevice,)


class SaveFile(QtCore.QSaveFile):
    pass
