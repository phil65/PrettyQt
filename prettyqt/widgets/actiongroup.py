from typing import Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    POLICIES = bidict(
        none=QtWidgets.QActionGroup.ExclusionPolicy(0),
        exclusive=QtWidgets.QActionGroup.ExclusionPolicy.Exclusive,
        exclusive_optional=QtWidgets.QActionGroup.ExclusionPolicy.ExclusiveOptional,
    )


QtWidgets.QActionGroup.__bases__ = (core.Object,)


class ActionGroup(QtWidgets.QActionGroup):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)

    def __len__(self) -> int:
        return len(self.actions())

    def __getitem__(self, item: int) -> QtWidgets.QAction:
        return self.actions()[item]

    def serialize_fields(self):
        return dict(exclusion_policy=self.get_exclusion_policy())

    def set_exclusion_policy(self, policy: Optional[str]):
        """Set exclusion policy to use.

        Allowed values are "none", "exclusive", "exclusive_optional"

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

    def get_exclusion_policy(self) -> str:
        """Return current exclusion policy.

        Possible values: "none", "exclusive", "exclusive_optional"

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
