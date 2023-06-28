from __future__ import annotations

from prettyqt import statemachine


class MouseEventTransition(
    statemachine.EventTransitionMixin, statemachine.QMouseEventTransition
):
    pass
