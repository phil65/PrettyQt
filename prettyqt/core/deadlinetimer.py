from __future__ import annotations

from prettyqt import constants
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


class DeadlineTimer(QtCore.QDeadlineTimer):
    def set_type(self, typ: constants.TimerTypeStr):
        """Set the timer type.

        Args:
            typ: timer type

        Raises:
            InvalidParamError: timer type does not exist
        """
        if typ not in constants.TIMER_TYPE:
            raise InvalidParamError(typ, constants.TIMER_TYPE)
        self.setTimerType(constants.TIMER_TYPE[typ])

    def get_type(self) -> constants.TimerTypeStr:
        """Return current timer type.

        Returns:
            timer type
        """
        return constants.TIMER_TYPE.inverse[self.timerType()]
