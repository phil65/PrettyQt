from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractEventDispatcher(core.ObjectMixin, QtCore.QAbstractEventDispatcher):
    pass
