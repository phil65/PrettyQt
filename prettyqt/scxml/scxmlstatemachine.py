from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtScxml


QtScxml.QScxmlStateMachine.__bases__ = (core.Object,)


class ScxmlStateMachine(QtScxml.QScxmlStateMachine):
    pass
