from __future__ import annotations

from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


sm = QtCore.QStateMachine

ERROR = bidict(
    none=sm.NoError,
    no_initial_state=sm.NoInitialStateError,
    no_default_state_in_history_state=sm.NoDefaultStateInHistoryStateError,
    no_common_ancestor_for_transistion=sm.NoCommonAncestorForTransitionError,
    state_machine_child_Mode_set_to_parallel=sm.StateMachineChildModeSetToParallelError,
)

ErrorStr = Literal[
    "none",
    "no_initial_state",
    "no_default_state_in_history_state",
    "no_common_ancestor_for_transistion",
    "state_machine_child_Mode_set_to_parallel",
]

PRIORITY = bidict(
    normal=sm.NormalPriority,
    high=sm.HighPriority,
)

PriorityStr = Literal["normal", "high"]

QtCore.QStateMachine.__bases__ = (core.State,)


class StateMachine(QtCore.QStateMachine):
    def __add__(self, other: QtCore.QAbstractState) -> StateMachine:
        self.addState(other)
        return self

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def post_event(self, event: QtCore.QEvent, priority: PriorityStr = "normal"):
        if priority not in PRIORITY:
            raise InvalidParamError(priority, PRIORITY)
        self.postEvent(event, PRIORITY[priority])

    def set_global_restore_policy(self, policy: core.state.RestorePolicyStr):
        """Set restore policy to use.

        Args:
            policy: restore policy to use

        Raises:
            InvalidParamError: restore policy does not exist
        """
        if policy not in core.state.RESTORE_POLICY:
            raise InvalidParamError(policy, core.state.RESTORE_POLICY)
        self.setGlobalRestorePolicy(core.state.RESTORE_POLICY[policy])

    def get_global_restore_policy(self) -> core.state.RestorePolicyStr:
        """Return current restore policy.

        Returns:
            restore policy
        """
        return core.state.RESTORE_POLICY.inverse[self.globalRestorePolicy()]
