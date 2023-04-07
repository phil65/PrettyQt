from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class ThreadPool(core.ObjectMixin, QtCore.QThreadPool):
    pass
