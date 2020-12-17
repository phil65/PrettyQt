from typing import Literal

from qtpy import QtCore

from prettyqt.utils import bidict


CLOCK_TYPE = bidict(
    system_time=QtCore.QElapsedTimer.SystemTime,
    monotonic_clock=QtCore.QElapsedTimer.MonotonicClock,
    tick_counter=QtCore.QElapsedTimer.TickCounter,
    mach_absolute_time=QtCore.QElapsedTimer.MachAbsoluteTime,
    performance_counter=QtCore.QElapsedTimer.PerformanceCounter,
)

ClockTypeStr = Literal[
    "system_time",
    "monotonic_clock",
    "tick_counter",
    "mach_absolute_time",
    "performance_counter",
]


class ElapsedTimer(QtCore.QElapsedTimer):
    def __bool__(self):
        return self.isValid()

    def get_clock_type(self) -> ClockTypeStr:
        """Return current clock type.

        Returns:
            clock type
        """
        return CLOCK_TYPE.inverse[self.clockType()]
