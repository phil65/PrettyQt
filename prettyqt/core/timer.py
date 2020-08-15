# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


QtCore.QTimer.__bases__ = (core.Object,)

TYPES = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)


class Timer(QtCore.QTimer):
    @classmethod
    def single_shot(cls, callback):
        timer = cls()
        timer.timeout.connect(callback)
        timer.setSingleShot(True)
        return timer

    def set_type(self, typ: str):
        """Set the timer type.

        Allowed values are "horizontal", "vertical"

        Args:
            typ: timer type

        Raises:
            InvalidParamError: timer type does not exist
        """
        if typ not in TYPES:
            raise InvalidParamError(typ, TYPES)
        self.setTimerType(TYPES[typ])

    def get_type(self) -> str:
        """Return current timer type.

        Possible values: "horizontal", "vertical"

        Returns:
            timer type
        """
        return TYPES.inv[self.timerType()]
