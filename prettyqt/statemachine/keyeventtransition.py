from prettyqt import statemachine


class KeyEventTransition(
    statemachine.AbstractTransitionMixin, statemachine.QKeyEventTransition
):
    pass
