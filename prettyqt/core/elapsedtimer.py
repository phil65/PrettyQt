from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


CLOCK_TYPE = bidict(
    system_time=QtCore.QElapsedTimer.ClockType.SystemTime,
    monotonic_clock=QtCore.QElapsedTimer.ClockType.MonotonicClock,
    tick_counter=QtCore.QElapsedTimer.ClockType.TickCounter,
    mach_absolute_time=QtCore.QElapsedTimer.ClockType.MachAbsoluteTime,
    performance_counter=QtCore.QElapsedTimer.ClockType.PerformanceCounter,
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
