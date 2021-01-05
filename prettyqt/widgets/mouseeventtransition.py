from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QMouseEventTransition.__bases__ = (core.EventTransition,)


class MouseEventTransition(QtWidgets.QMouseEventTransition):
    pass
