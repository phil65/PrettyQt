from __future__ import annotations

from prettyqt import constants
from prettyqt.qt import QtCore


class BasicTimer(QtCore.QBasicTimer):
    def __bool__(self):
        return self.isActive()

    def start_timer(
        self, msec: int, obj: QtCore.QObject, timer_type: constants.TimerTypeStr
    ):
        self.start(msec, constants.TIMER_TYPE.get_enum_value(timer_type), obj)
