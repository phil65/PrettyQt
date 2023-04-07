from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class Buffer(core.IODeviceMixin, QtCore.QBuffer):
    pass
