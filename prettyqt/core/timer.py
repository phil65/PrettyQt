from __future__ import annotations

from typing import Callable

from qtpy import QtCore

from prettyqt import constants, core
from prettyqt.utils import InvalidParamError


QtCore.QTimer.__bases__ = (core.Object,)


class Timer(QtCore.QTimer):
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
