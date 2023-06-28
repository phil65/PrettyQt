from __future__ import annotations

from prettyqt import statemachine


class KeyEventTransition(
    statemachine.EventTransitionMixin, statemachine.QKeyEventTransition
):
    pass
