from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine
from prettyqt.utils import bidict


ChildModeStr = Literal["exclusive", "parallel"]

CHILD_MODE: bidict[ChildModeStr, QtStateMachine.QState.ChildMode] = bidict(
    exclusive=QtStateMachine.QState.ChildMode.ExclusiveStates,
    parallel=QtStateMachine.QState.ChildMode.ParallelStates,
)

RestorePolicyStr = Literal["dont_restore", "restore"]

RESTORE_POLICY: bidict[RestorePolicyStr, QtStateMachine.QState.RestorePolicy] = bidict(
    dont_restore=QtStateMachine.QState.RestorePolicy.DontRestoreProperties,
    restore=QtStateMachine.QState.RestorePolicy.RestoreProperties,
)


class StateMixin(statemachine.AbstractStateMixin):
    def set_child_mode(self, mode: ChildModeStr | QtStateMachine.QState.ChildMode):
        """Set child mode to use.

        Args:
            mode: child mode to use
        """
        self.setChildMode(CHILD_MODE.get_enum_value(mode))

    def get_child_mode(self) -> ChildModeStr:
        """Return current child mode.

        Returns:
            child mode
        """
        return CHILD_MODE.inverse[self.childMode()]


class State(StateMixin, QtStateMachine.QState):
    pass


if __name__ == "__main__":
    reg = State()
