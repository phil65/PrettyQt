from qtpy import QtCore

from prettyqt import core


QtCore.QFinalState.__bases__ = (core.AbstractState,)


class FinalState(QtCore.QFinalState):
    pass
