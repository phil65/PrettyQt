from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtStateMachine
from prettyqt.utils import InvalidParamError, bidict


TRANSITION_TYPE = bidict(
    exclusive=QtStateMachine.QAbstractTransition.ExternalTransition,
    parallel=QtStateMachine.QAbstractTransition.InternalTransition,
)

TransitionTypeStr = Literal["exclusive", "parallel"]

QtStateMachine.QAbstractTransition.__bases__ = (core.Object,)


class AbstractTransition(QtStateMachine.QAbstractTransition):
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
