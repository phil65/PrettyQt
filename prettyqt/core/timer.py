from __future__ import annotations

from prettyqt import constants, core
from prettyqt.utils import helpers


class Timer(core.ObjectMixin, core.QTimer):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"timerType": constants.TIMER_TYPE}
        return maps

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
    timer = Timer(timeout=print)
    timer.set_interval("2m")
