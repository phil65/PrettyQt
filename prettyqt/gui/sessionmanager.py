from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


RESTART_HINT = bidict(
    if_running=QtGui.QSessionManager.RestartHint.RestartIfRunning,
    anyway=QtGui.QSessionManager.RestartHint.RestartAnyway,
    immediately=QtGui.QSessionManager.RestartHint.RestartImmediately,
    never=QtGui.QSessionManager.RestartHint.RestartNever,
)

RestartHintStr = Literal["if_running", "anyway", "immediately", "never"]


QtGui.QSessionManager.__bases__ = (core.Object,)


class SessionManager:
    def __init__(self, item: QtGui.QSessionManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_restart_hint(self, style: RestartHintStr):
        """Set the restart hint.

        Args:
            style: restart hint

        Raises:
            InvalidParamError: restart hint does not exist
        """
        if style not in RESTART_HINT:
            raise InvalidParamError(style, RESTART_HINT)
        self.setRestartHint(RESTART_HINT[style])

    def get_restart_hint(self) -> RestartHintStr:
        """Return current restart hint.

        Returns:
            restart hint
        """
        return RESTART_HINT.inverse[self.restartHint()]
