from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.qt import QtCore, QtStateMachine
from prettyqt.utils import bidict


sm = QtStateMachine.QStateMachine.Error

ErrorStr = Literal[
    "none",
    "no_initial_state",
    "no_default_state_in_history_state",
    "no_common_ancestor_for_transistion",
    "state_machine_child_Mode_set_to_parallel",
]

ERROR: bidict[ErrorStr, sm] = bidict(
    none=sm.NoError,
    no_initial_state=sm.NoInitialStateError,
    no_default_state_in_history_state=sm.NoDefaultStateInHistoryStateError,
    no_common_ancestor_for_transistion=sm.NoCommonAncestorForTransitionError,
    state_machine_child_Mode_set_to_parallel=sm.StateMachineChildModeSetToParallelError,
)

PriorityStr = Literal["normal", "high"]

PRIORITY: bidict[PriorityStr, QtStateMachine.QStateMachine.EventPriority] = bidict(
    normal=QtStateMachine.QStateMachine.EventPriority.NormalPriority,
    high=QtStateMachine.QStateMachine.EventPriority.HighPriority,
)


class StateMachine(statemachine.state.StateMixin, QtStateMachine.QStateMachine):
    def __add__(self, other: QtStateMachine.QAbstractState) -> StateMachine:
        self.addState(other)
        return self

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def post_event(
        self,
        event: QtCore.QEvent,
        priority: PriorityStr | QtStateMachine.QStateMachine.EventPriority = "normal",
    ):
        self.postEvent(event, PRIORITY.get_enum_value(priority))

    def set_global_restore_policy(
        self,
        policy: statemachine.state.RestorePolicyStr | statemachine.State.RestorePolicy,
    ):
        """Set restore policy to use.

        Args:
            policy: restore policy to use
        """
        self.setGlobalRestorePolicy(
            statemachine.state.RESTORE_POLICY.get_enum_value(policy)
        )

    def get_global_restore_policy(self) -> statemachine.state.RestorePolicyStr:
        """Return current restore policy.

        Returns:
            restore policy
        """
        return statemachine.state.RESTORE_POLICY.inverse[self.globalRestorePolicy()]
