# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


CHILD_MODES = bidict(
    exclusive=QtCore.QState.ExclusiveStates, parallel=QtCore.QState.ParallelStates
)

RESTORE_POLICIES = bidict(
    dont_restore=QtCore.QState.DontRestoreProperties,
    restore=QtCore.QState.RestoreProperties,
)

QtCore.QState.__bases__ = (core.AbstractState,)


class State(QtCore.QState):
    def set_child_mode(self, mode: str):
        """Set child mode to use.

        Allowed values are "exclusive", "parallel"

        Args:
            mode: child mode to use

        Raises:
            InvalidParamError: child mode does not exist
        """
        if mode not in CHILD_MODES:
            raise InvalidParamError(mode, CHILD_MODES)
        self.setChildMode(CHILD_MODES[mode])

    def get_child_mode(self) -> str:
        """Return current child mode.

        Possible values: "exclusive", "parallel"

        Returns:
            child mode
        """
        return CHILD_MODES.inv[self.childMode()]


if __name__ == "__main__":
    reg = State()
