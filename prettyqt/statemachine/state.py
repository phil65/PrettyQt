from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.utils import bidict


ChildModeStr = Literal["exclusive", "parallel"]

CHILD_MODE: bidict[ChildModeStr, statemachine.QState.ChildMode] = bidict(
    exclusive=statemachine.QState.ChildMode.ExclusiveStates,
    parallel=statemachine.QState.ChildMode.ParallelStates,
)

RestorePolicyStr = Literal["dont_restore", "restore"]

RESTORE_POLICY: bidict[RestorePolicyStr, statemachine.QState.RestorePolicy] = bidict(
    dont_restore=statemachine.QState.RestorePolicy.DontRestoreProperties,
    restore=statemachine.QState.RestorePolicy.RestoreProperties,
)


class StateMixin(statemachine.AbstractStateMixin):
    def set_child_mode(self, mode: ChildModeStr | statemachine.QState.ChildMode):
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


class State(StateMixin, statemachine.QState):
    pass


if __name__ == "__main__":
    reg = State()
