from typing import Literal

from qtpy import QtCore

from prettyqt.utils import bidict, InvalidParamError


TYPE = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)

TypeStr = Literal["precise", "coarse", "very_coarse"]


class DeadlineTimer(QtCore.QDeadlineTimer):
    def set_type(self, typ: TypeStr):
        """Set the timer type.

        Allowed values are "precise", "coarse", "very_coarse"

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

        Possible values: "precise", "coarse", "very_coarse"

        Returns:
            timer type
        """
        return TYPE.inverse[self.timerType()]
