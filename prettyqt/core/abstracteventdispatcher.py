from prettyqt import core


class AbstractEventDispatcher(core.ObjectMixin, core.QAbstractEventDispatcher):
    """Interface to manage Qt's event queue."""
