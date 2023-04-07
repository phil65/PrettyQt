from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class SaveFile(core.FileDeviceMixin, QtCore.QSaveFile):
    pass
