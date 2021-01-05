from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QSignalTransition.__bases__ = (core.AbstractTransition,)


class SignalTransition(QtCore.QSignalTransition):
    pass
