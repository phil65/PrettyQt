from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


POLICIES = bidict(
    none=QtWidgets.QActionGroup.ExclusionPolicy.None_,
    exclusive=QtWidgets.QActionGroup.ExclusionPolicy.Exclusive,
    exclusive_optional=QtWidgets.QActionGroup.ExclusionPolicy.ExclusiveOptional,
)

ExclusionPolicyStr = Literal["none", "exclusive", "exclusive_optional"]


QtWidgets.QActionGroup.__bases__ = (core.Object,)


class ActionGroup(QtWidgets.QActionGroup):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)  # type: ignore

    def __len__(self) -> int:
        return len(self.actions())

    def __getitem__(self, item: int) -> QtWidgets.QAction:
        return self.actions()[item]

    def serialize_fields(self):
        return dict(
            exclusion_policy=self.get_exclusion_policy(),
            visible=self.isVisible(),
            enabled=self.isEnabled(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setEnabled(state.get("enabled", ""))
        self.setVisible(state.get("visible", ""))
        self.set_exclusion_policy(state.get("exclusion_policy", ""))

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
    from prettyqt import widgets

    app = widgets.app()
    action = ActionGroup()
    act = widgets.Action()
    action.addAction(act)
    print(act in action)
    app.main_loop()
