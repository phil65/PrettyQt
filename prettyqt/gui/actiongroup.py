from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


ExclusionPolicyStr = Literal["none", "exclusive", "exclusive_optional"]

EXCLUSION_POLICY: bidict[ExclusionPolicyStr, QtGui.QActionGroup.ExclusionPolicy] = bidict(
    none=QtGui.QActionGroup.ExclusionPolicy.None_,
    exclusive=QtGui.QActionGroup.ExclusionPolicy.Exclusive,
    exclusive_optional=QtGui.QActionGroup.ExclusionPolicy.ExclusiveOptional,
)


class ActionGroup(core.ObjectMixin, QtGui.QActionGroup):
    def __init__(self, parent: core.QObject | None = None, **kwargs):
        super().__init__(parent, **kwargs)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"exclusionPolicy": EXCLUSION_POLICY}
        return maps

    def __len__(self) -> int:
        return len(self.actions())

    def __getitem__(self, item: int) -> QtGui.QAction:
        return self.actions()[item]

    def set_exclusion_policy(
        self, policy: ExclusionPolicyStr | QtGui.QActionGroup.ExclusionPolicy | None
    ):
        """Set exclusion policy to use.

        Args:
            policy: exclusion policy to use
        """
        if policy is None:
            policy = "none"
        self.setExclusionPolicy(EXCLUSION_POLICY.get_enum_value(policy))

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
