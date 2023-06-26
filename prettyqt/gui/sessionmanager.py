from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


RestartHintStr = Literal["if_running", "anyway", "immediately", "never"]

RESTART_HINT: bidict[RestartHintStr, QtGui.QSessionManager.RestartHint] = bidict(
    if_running=QtGui.QSessionManager.RestartHint.RestartIfRunning,
    anyway=QtGui.QSessionManager.RestartHint.RestartAnyway,
    immediately=QtGui.QSessionManager.RestartHint.RestartImmediately,
    never=QtGui.QSessionManager.RestartHint.RestartNever,
)


class SessionManager(core.ObjectMixin):
    def __init__(self, item: QtGui.QSessionManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_restart_hint(self, style: RestartHintStr | QtGui.QSessionManager.RestartHint):
        """Set the restart hint.

        Args:
            style: restart hint
        """
        self.setRestartHint(RESTART_HINT.get_enum_value(style))

    def get_restart_hint(self) -> RestartHintStr:
        """Return current restart hint.

        Returns:
            restart hint
        """
        return RESTART_HINT.inverse[self.restartHint()]
