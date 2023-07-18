from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtScxml


class ScxmlInvokableService(core.ObjectMixin, QtScxml.QScxmlInvokableService):
    """The base class for services called from state machines."""
