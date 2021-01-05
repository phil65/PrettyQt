from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QKeyEventTransition.__bases__ = (core.EventTransition,)


class KeyEventTransition(QtWidgets.QKeyEventTransition):
    pass
