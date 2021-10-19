from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


QtStateMachine.QKeyEventTransition.__bases__ = (statemachine.EventTransition,)


class KeyEventTransition(QtStateMachine.QKeyEventTransition):
    pass
