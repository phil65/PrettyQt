# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt.utils import bidict, InvalidParamError


TYPES = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)


class BasicTimer(QtCore.QBasicTimer):
    def __bool__(self):
        return self.isActive()

    def start_timer(self, msec: int, obj: QtCore.QObject, timer_type: str):
        if timer_type not in TYPES:
            raise InvalidParamError(timer_type, TYPES)
        self.start(msec, TYPES[timer_type], obj)
