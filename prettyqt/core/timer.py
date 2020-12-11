from __future__ import annotations

from typing import Literal, Callable

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


QtCore.QTimer.__bases__ = (core.Object,)

TYPE = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)

TypeStr = Literal["precise", "coarse", "very_coarse"]


class Timer(QtCore.QTimer):
    @classmethod
    def single_shot(cls, callback: Callable) -> Timer:
        timer = cls()
        timer.timeout.connect(callback)
        timer.setSingleShot(True)
        return timer

    def set_type(self, typ: TypeStr):
        """Set the timer type.

        Args:
            typ: timer type

        Raises:
            InvalidParamError: timer type does not exist
        """
        if typ not in TYPE:
            raise InvalidParamError(typ, TYPE)
        self.setTimerType(TYPE[typ])

    def get_type(self) -> TypeStr:
        """Return current timer type.

        Returns:
            timer type
        """
        return TYPE.inverse[self.timerType()]
