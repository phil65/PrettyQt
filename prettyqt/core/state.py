from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


CHILD_MODE = bidict(
    exclusive=QtCore.QState.ExclusiveStates, parallel=QtCore.QState.ParallelStates
)

ChildModeStr = Literal["exclusive", "parallel"]

RESTORE_POLICY = bidict(
    dont_restore=QtCore.QState.DontRestoreProperties,
    restore=QtCore.QState.RestoreProperties,
)

RestorePolicyStr = Literal["dont_restore", "restore"]


QtCore.QState.__bases__ = (core.AbstractState,)


class State(QtCore.QState):
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
