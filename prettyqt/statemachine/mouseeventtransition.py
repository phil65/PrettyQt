from __future__ import annotations

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine


class MouseEventTransition(
    statemachine.EventTransitionMixin, QtStateMachine.QMouseEventTransition
):
    pass
