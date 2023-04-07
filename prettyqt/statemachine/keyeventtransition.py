from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


class KeyEventTransition(
    statemachine.EventTransitionMixin, QtStateMachine.QKeyEventTransition
):
    pass
