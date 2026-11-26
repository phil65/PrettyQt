from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.qt import QtStateMachine
from prettyqt.utils import bidict


TransitionTypeStr = Literal["exclusive", "parallel"]

TRANSITION_TYPE: bidict[
    TransitionTypeStr, QtStateMachine.QAbstractTransition.TransitionType
] = bidict(
    exclusive=QtStateMachine.QAbstractTransition.TransitionType.ExternalTransition,
    parallel=QtStateMachine.QAbstractTransition.TransitionType.InternalTransition,
)


if TYPE_CHECKING:
    _AbstractTransitionBase = QtStateMachine.QAbstractTransition
else:
    _AbstractTransitionBase = object


class AbstractTransitionMixin(core.ObjectMixin, _AbstractTransitionBase):
    def set_transition_type(
        self, typ: TransitionTypeStr | QtStateMachine.QAbstractTransition.TransitionType
    ):
        """Set transition type.

        Args:
            typ: transition type to use
        """
        self.setTransitionType(TRANSITION_TYPE.get_enum_value(typ))

    def get_transition_type(self) -> TransitionTypeStr:
        """Return current transition type.

        Returns:
            transition type
        """
        return TRANSITION_TYPE.inverse[self.transitionType()]


class AbstractTransition(AbstractTransitionMixin, QtStateMachine.QAbstractTransition):
    pass
