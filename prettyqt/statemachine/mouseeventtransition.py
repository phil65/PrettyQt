from prettyqt import statemachine


class MouseEventTransition(
    statemachine.AbstractTransitionMixin, statemachine.QMouseEventTransition
):
    pass
