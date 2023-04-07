from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class TemporaryFile(core.FileMixin, QtCore.QTemporaryFile):
    pass
