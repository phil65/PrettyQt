from __future__ import annotations

from typing import Callable

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, helpers


QtCore.QTimer.__bases__ = (core.Object,)


class Timer(QtCore.QTimer):
    def serialize_fields(self):
        return dict(
            interval=self.interval(),
            single_shot=self.isSingleShot(),
            timer_type=self.get_type(),
        )

    @classmethod
    def single_shot(cls, callback: Callable) -> Timer:
        timer = cls()
        timer.timeout.connect(callback)
        timer.setSingleShot(True)
        return timer

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

    def set_interval(self, interval: int | str):
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        self.setInterval(interval)

    def start_timer(self, interval: None | int | str = None):
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        if interval is None:
            self.start()
        else:
            self.start(interval)

    def restart(self):
        self.stop()
        self.start()


if __name__ == "__main__":
    timer = Timer()
    timer.set_interval("2m")
