from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtScxml


class ScxmlStateMachine(core.ObjectMixin, QtScxml.QScxmlStateMachine):
    """Interface to the state machines created from SCXML files."""
