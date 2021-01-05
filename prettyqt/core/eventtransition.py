from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QEventTransition.__bases__ = (core.AbstractTransition,)


class EventTransition(QtCore.QEventTransition):
    pass
