from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.qt import QtStateMachine
from prettyqt.utils import bidict


TransitionTypeStr = Literal["external", "internal"]

TRANSITION_TYPE: bidict[
    TransitionTypeStr, QtStateMachine.QAbstractTransition.TransitionType
] = bidict(
    external=QtStateMachine.QAbstractTransition.TransitionType.ExternalTransition,
    internal=QtStateMachine.QAbstractTransition.TransitionType.InternalTransition,
)


if TYPE_CHECKING:
    _AbstractTransitionBase = QtStateMachine.QAbstractTransition
else:
    _AbstractTransitionBase = object


class AbstractTransitionMixin(core.ObjectMixin, _AbstractTransitionBase):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"transitionType": TRANSITION_TYPE}
        return maps

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
