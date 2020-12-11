from qtpy import QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

RESTART_HINT = bidict(
    if_running=QtGui.QSessionManager.RestartIfRunning,
    anyway=QtGui.QSessionManager.RestartAnyway,
    immediately=QtGui.QSessionManager.RestartImmediately,
    never=QtGui.QSessionManager.RestartNever,
)


QtGui.QSessionManager.__bases__ = (core.Object,)


class SessionManager:
    def __init__(self, item: QtGui.QSessionManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_restart_hint(self, style: str):
        """Set the restart hint.

        Allowed values are "if_running", "anyway", "immediatly", "never"

        Args:
            style: restart hint

        Raises:
            InvalidParamError: restart hint does not exist
        """
        if style not in RESTART_HINT:
            raise InvalidParamError(style, RESTART_HINT)
        self.setRestartHint(RESTART_HINT[style])

    def get_restart_hint(self) -> str:
        """Return current restart hint.

        Possible values: "if_running", "anyway", "immediatly", "never"

        Returns:
            restart hint
        """
        return RESTART_HINT.inverse[self.restartHint()]
