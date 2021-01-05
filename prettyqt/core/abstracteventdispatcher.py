from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QAbstractEventDispatcher.__bases__ = (core.Object,)


class AbstractEventDispatcher(QtCore.QAbstractEventDispatcher):
    pass
