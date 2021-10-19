from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


QtStateMachine.QMouseEventTransition.__bases__ = (statemachine.EventTransition,)


class MouseEventTransition(QtStateMachine.QMouseEventTransition):
    pass
