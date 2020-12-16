from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


TRANSITION_TYPE = bidict(
    exclusive=QtCore.QAbstractTransition.ExternalTransition,
    parallel=QtCore.QAbstractTransition.InternalTransition,
)

TransitionTypeStr = Literal["exclusive", "parallel"]

QtCore.QAbstractTransition.__bases__ = (core.Object,)


class AbstractTransition(QtCore.QAbstractTransition):
    def set_transition_type(self, typ: TransitionTypeStr):
        """Set transition type.

        Args:
            typ: transition type to use

        Raises:
            InvalidParamError: transition type does not exist
        """
        if typ not in TRANSITION_TYPE:
            raise InvalidParamError(typ, TRANSITION_TYPE)
        self.setTransitionType(TRANSITION_TYPE[typ])

    def get_transition_type(self) -> TransitionTypeStr:
        """Return current transition type.

        Returns:
            transition type
        """
        return TRANSITION_TYPE.inverse[self.transitionType()]
