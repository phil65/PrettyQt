from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class FileMixin(core.FileDeviceMixin):
    pass


class File(FileMixin, QtCore.QFile):
    pass
