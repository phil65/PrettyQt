from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


class FinalState(statemachine.AbstractStateMixin, QtStateMachine.QFinalState):
    pass
