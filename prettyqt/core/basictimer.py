from typing import Literal

from qtpy import QtCore

from prettyqt.utils import bidict, InvalidParamError


TYPE = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)

TypeStr = Literal["precise", "coarse", "very_coarse"]


class BasicTimer(QtCore.QBasicTimer):
    def __bool__(self):
        return self.isActive()

    def start_timer(self, msec: int, obj: QtCore.QObject, timer_type: TypeStr):
        if timer_type not in TYPE:
            raise InvalidParamError(timer_type, TYPE)
        self.start(msec, TYPE[timer_type], obj)
