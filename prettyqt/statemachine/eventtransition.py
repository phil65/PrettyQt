from prettyqt import statemachine


class EventTransition(
    statemachine.AbstractTransitionMixin, statemachine.QEventTransition
):
    pass
