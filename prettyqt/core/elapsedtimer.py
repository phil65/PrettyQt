# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt.utils import bidict


TYPES = bidict(
    system_time=QtCore.QElapsedTimer.SystemTime,
    monotonic_clock=QtCore.QElapsedTimer.MonotonicClock,
    tick_counter=QtCore.QElapsedTimer.TickCounter,
    mach_absolute_time=QtCore.QElapsedTimer.MachAbsoluteTime,
    performance_counter=QtCore.QElapsedTimer.PerformanceCounter,
)


class ElapsedTimer(QtCore.QElapsedTimer):
    def __bool__(self):
        return self.isValid()

    def get_clock_type(self) -> str:
        """Return current clock type.

        Possible values: "system_time", "monotonic_clock", "tick_counter",
                         "mach_absolute_time", "performance_counter"

        Returns:
            clock type
        """
        return TYPES.inv[self.clockType()]
