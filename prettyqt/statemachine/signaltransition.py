from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


class SignalTransition(
    statemachine.AbstractTransitionMixin, QtStateMachine.QSignalTransition
):
    pass
