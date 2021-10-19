from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


QtStateMachine.QFinalState.__bases__ = (statemachine.AbstractState,)


class FinalState(QtStateMachine.QFinalState):
    pass
