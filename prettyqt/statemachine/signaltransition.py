from __future__ import annotations

from prettyqt import statemachine


class SignalTransition(
    statemachine.AbstractTransitionMixin, statemachine.QSignalTransition
):
    pass
