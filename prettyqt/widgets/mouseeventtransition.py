from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QMouseEventTransition.__bases__ = (core.EventTransition,)


class MouseEventTransition(QtWidgets.QMouseEventTransition):
    pass
