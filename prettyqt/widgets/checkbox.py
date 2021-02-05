from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QCheckBox.__bases__ = (widgets.AbstractButton,)


class CheckBox(QtWidgets.QCheckBox):

    value_changed = core.Signal(int)

    def __init__(
        self,
        label: str = "",
        parent: QtWidgets.QWidget | None = None,
        checked: bool = False,
    ):
        super().__init__(label, parent)
        self.stateChanged.connect(self.value_changed)
        self.setChecked(checked)

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setTristate(state.get("is_tristate", False))
        self.set_checkstate(state["checkstate"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(
            checkstate=self.get_checkstate(),
            is_tristate=self.isTristate(),
        )

    def set_checkstate(self, state: constants.StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in constants.STATE:
            raise InvalidParamError(state, constants.STATE)
        self.setCheckState(constants.STATE[state])

    def get_checkstate(self) -> constants.StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.STATE.inverse[self.checkState()]


if __name__ == "__main__":
    app = widgets.app()
    widget = CheckBox("test")
    widget.show()
    app.main_loop()
