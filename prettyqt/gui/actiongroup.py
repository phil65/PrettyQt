from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict


EXCLUSION_POLICY = bidict(
    none=QtGui.QActionGroup.ExclusionPolicy.None_,
    exclusive=QtGui.QActionGroup.ExclusionPolicy.Exclusive,
    exclusive_optional=QtGui.QActionGroup.ExclusionPolicy.ExclusiveOptional,
)

ExclusionPolicyStr = Literal["none", "exclusive", "exclusive_optional"]


class ActionGroup(core.ObjectMixin, QtGui.QActionGroup):
    def __init__(self, parent: QtCore.QObject | None = None, **kwargs):
        super().__init__(parent, **kwargs)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"exclusionPolicy": EXCLUSION_POLICY}
        return maps

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
        if policy not in EXCLUSION_POLICY:
            raise InvalidParamError(policy, EXCLUSION_POLICY)
        self.setExclusionPolicy(EXCLUSION_POLICY[policy])

    def get_exclusion_policy(self) -> ExclusionPolicyStr:
        """Return current exclusion policy.

        Returns:
            exclusion policy
        """
        return EXCLUSION_POLICY.inverse[self.exclusionPolicy()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    action = ActionGroup()
    act = gui.Action()
    action.addAction(act)
    app.exec()
