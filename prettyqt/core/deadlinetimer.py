from __future__ import annotations

from prettyqt import constants
from prettyqt.qt import QtCore


class DeadlineTimer(QtCore.QDeadlineTimer):
    """Marks a deadline in the future."""

    def set_type(self, typ: constants.TimerTypeStr | constants.TimerType):
        """Set the timer type.

        Args:
            typ: timer type
        """
        self.setTimerType(constants.TIMER_TYPE.get_enum_value(typ))

    def get_type(self) -> constants.TimerTypeStr:
        """Return current timer type.

        Returns:
            timer type
        """
        return constants.TIMER_TYPE.inverse[self.timerType()]
