from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict


POLICIES = bidict(
    none=QtGui.QActionGroup.ExclusionPolicy.None_,
    exclusive=QtGui.QActionGroup.ExclusionPolicy.Exclusive,
    exclusive_optional=QtGui.QActionGroup.ExclusionPolicy.ExclusiveOptional,
)

ExclusionPolicyStr = Literal["none", "exclusive", "exclusive_optional"]


class ActionGroup(core.ObjectMixin, QtGui.QActionGroup):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)  # type: ignore

    def __len__(self) -> int:
        return len(self.actions())

    def __getitem__(self, item: int) -> QtGui.QAction:
        return self.actions()[item]

    def set_exclusion_policy(self, policy: ExclusionPolicyStr | None):
        """Set exclusion policy to use.

        Args:
            policy: exclusion policy to use

        Raises:
            InvalidParamError: exclusion policy does not exist
        """
        if policy is None:
            policy = "none"
        if policy not in POLICIES:
            raise InvalidParamError(policy, POLICIES)
        self.setExclusionPolicy(POLICIES[policy])

    def get_exclusion_policy(self) -> ExclusionPolicyStr:
        """Return current exclusion policy.

        Returns:
            exclusion policy
        """
        return POLICIES.inverse[self.exclusionPolicy()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    action = ActionGroup()
    act = gui.Action()
    action.addAction(act)
    print(act in action)
    app.main_loop()
