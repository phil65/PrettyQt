from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


QtStateMachine.QSignalTransition.__bases__ = (statemachine.AbstractTransition,)


class SignalTransition(QtStateMachine.QSignalTransition):
    pass
