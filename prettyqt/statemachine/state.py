from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine
from prettyqt.utils import InvalidParamError, bidict


CHILD_MODE = bidict(
    exclusive=QtStateMachine.QState.ChildMode.ExclusiveStates,
    parallel=QtStateMachine.QState.ChildMode.ParallelStates,
)

ChildModeStr = Literal["exclusive", "parallel"]

RESTORE_POLICY = bidict(
    dont_restore=QtStateMachine.QState.RestorePolicy.DontRestoreProperties,
    restore=QtStateMachine.QState.RestorePolicy.RestoreProperties,
)

RestorePolicyStr = Literal["dont_restore", "restore"]


QtStateMachine.QState.__bases__ = (statemachine.AbstractState,)


class State(QtStateMachine.QState):
    def set_child_mode(self, mode: ChildModeStr):
        """Set child mode to use.

        Args:
            mode: child mode to use

        Raises:
            InvalidParamError: child mode does not exist
        """
        if mode not in CHILD_MODE:
            raise InvalidParamError(mode, CHILD_MODE)
        self.setChildMode(CHILD_MODE[mode])

    def get_child_mode(self) -> ChildModeStr:
        """Return current child mode.

        Returns:
            child mode
        """
        return CHILD_MODE.inverse[self.childMode()]


if __name__ == "__main__":
    reg = State()
