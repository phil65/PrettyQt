from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QFinalState.__bases__ = (core.AbstractState,)


class FinalState(QtCore.QFinalState):
    pass
