from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QThreadPool.__bases__ = (core.Object,)


class ThreadPool(QtCore.QThreadPool):
    pass
