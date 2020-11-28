# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt.utils import bidict, InvalidParamError


TYPES = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)


class DeadlineTimer(QtCore.QDeadlineTimer):
    def set_type(self, typ: str):
        """Set the timer type.

        Allowed values are "precise", "coarse", "very_coarse"

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

        Possible values: "precise", "coarse", "very_coarse"

        Returns:
            timer type
        """
        return TYPES.inv[self.timerType()]
