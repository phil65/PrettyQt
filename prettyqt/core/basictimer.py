from __future__ import annotations

from prettyqt import constants, core


class BasicTimer(core.QBasicTimer):
    """Timer events for objects."""

    def __bool__(self):
        return self.isActive()

    def start_timer(
        self, msec: int, obj: core.QObject, timer_type: constants.TimerTypeStr
    ):
        self.start(msec, constants.TIMER_TYPE.get_enum_value(timer_type), obj)
