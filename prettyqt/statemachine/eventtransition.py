from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


class EventTransition(
    statemachine.AbstractTransitionMixin, QtStateMachine.QEventTransition
):
    pass
