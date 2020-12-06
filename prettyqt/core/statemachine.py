# -*- coding: utf-8 -*-

from __future__ import annotations

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

sm = QtCore.QStateMachine

ERROR = bidict(
    none=sm.NoError,
    no_initial_state=sm.NoInitialStateError,
    no_default_state_in_history_state=sm.NoDefaultStateInHistoryStateError,
    no_common_ancestor_for_transistion=sm.NoCommonAncestorForTransitionError,
    state_machine_child_Mode_set_to_parallel=sm.StateMachineChildModeSetToParallelError,
)

PRIORITY = bidict(
    normal=sm.NormalPriority,
    high=sm.HighPriority,
)


QtCore.QStateMachine.__bases__ = (core.State,)


class StateMachine(QtCore.QStateMachine):
    def __add__(self, other: QtCore.QAbstractState) -> StateMachine:
        self.addState(other)
        return self

    def get_error(self) -> str:
        return ERROR.inv[self.error()]

    def post_event(self, event: QtCore.QEvent, priority: str = "normal"):
        if priority not in PRIORITY:
            raise InvalidParamError(priority, PRIORITY)
        self.postEvent(event, PRIORITY[priority])

    def set_global_restore_policy(self, policy: str):
        """Set restore policy to use.

        Allowed values are "restore", "dont_restore"

        Args:
            policy: restore policy to use

        Raises:
            InvalidParamError: restore policy does not exist
        """
        if policy not in core.state.RESTORE_POLICY:
            raise InvalidParamError(policy, core.state.RESTORE_POLICY)
        self.setGlobalRestorePolicy(core.state.RESTORE_POLICY[policy])

    def get_global_restore_policy(self) -> str:
        """Return current restore policy.

        Possible values: "restore", "dont_restore"

        Returns:
            restore policy
        """
        return core.state.RESTORE_POLICY.inv[self.globalRestorePolicy()]
