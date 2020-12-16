from qtpy import QtCore

from prettyqt import core


QtCore.QEventTransition.__bases__ = (core.AbstractTransition,)


class EventTransition(QtCore.QEventTransition):
    pass
