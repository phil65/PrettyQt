# -*- coding: utf-8 -*-
"""
"""

from typing import Optional

from qtpy import QtWidgets

from prettyqt import core
from prettyqt.utils import bidict


POLICIES = bidict(
    none=QtWidgets.QActionGroup.ExclusionPolicy(0),
    exclusive=QtWidgets.QActionGroup.ExclusionPolicy.Exclusive,
    exclusive_optional=QtWidgets.QActionGroup.ExclusionPolicy.ExclusiveOptional,
)


QtWidgets.QActionGroup.__bases__ = (core.Object,)


class ActionGroup(QtWidgets.QActionGroup):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

    def __len__(self) -> int:
        return len(self.actions())

    def __getitem__(self, item: int):
        return self.actions()[item]

    def set_exclusion_policy(self, policy: Optional[str]):
        """set exclusion policy to use

        Allowed values are "none", "exclusive", "exclusive_optional"

        Args:
            policy: exclusion policy to use

        Raises:
            ValueError: exclusion policy does not exist
        """
        if policy is None:
            policy = "none"
        if policy not in POLICIES:
            raise ValueError(f"Invalid exclusion policy. Valid values: {POLICIES.keys()}")
        self.setExclusionPolicy(POLICIES[policy])

    def get_exclusion_policy(self) -> str:
        """returns current exclusion policy

        Possible values: "none", "exclusive", "exclusive_optional"

        Returns:
            exclusion policy
        """
        return POLICIES.inv[self.exclusionPolicy()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    action = ActionGroup()
    act = widgets.Action()
    action.addAction(act)
    print(act in action)
    app.exec_()
