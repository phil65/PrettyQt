from prettyqt import statemachine


class KeyEventTransition(
    statemachine.EventTransitionMixin, statemachine.QKeyEventTransition
):
    pass
