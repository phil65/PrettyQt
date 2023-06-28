from __future__ import annotations

from prettyqt import statemachine


class EventTransition(
    statemachine.AbstractTransitionMixin, statemachine.QEventTransition
):
    pass
