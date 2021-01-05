from __future__ import annotations

from prettyqt import constants
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


class BasicTimer(QtCore.QBasicTimer):
    def __bool__(self):
        return self.isActive()

    def start_timer(
        self, msec: int, obj: QtCore.QObject, timer_type: constants.TimerTypeStr
    ):
        if timer_type not in constants.TIMER_TYPE:
            raise InvalidParamError(timer_type, constants.TIMER_TYPE)
        self.start(msec, constants.TIMER_TYPE[timer_type], obj)
