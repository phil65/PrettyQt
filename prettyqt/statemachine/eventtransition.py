from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


QtStateMachine.QEventTransition.__bases__ = (statemachine.AbstractTransition,)


class EventTransition(QtStateMachine.QEventTransition):
    pass
