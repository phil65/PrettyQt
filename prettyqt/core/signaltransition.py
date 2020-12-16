from qtpy import QtCore

from prettyqt import core


QtCore.QSignalTransition.__bases__ = (core.AbstractTransition,)


class SignalTransition(QtCore.QSignalTransition):
    pass
