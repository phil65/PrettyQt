from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QKeyEventTransition.__bases__ = (core.EventTransition,)


class KeyEventTransition(QtWidgets.QKeyEventTransition):
    pass
