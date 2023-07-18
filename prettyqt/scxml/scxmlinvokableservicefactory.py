from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtScxml


class ScxmlInvokableServiceFactory(
    core.ObjectMixin, QtScxml.QScxmlInvokableServiceFactory
):
    """Creates invokable service instances."""
