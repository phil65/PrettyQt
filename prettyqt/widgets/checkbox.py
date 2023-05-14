from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


class CheckBox(widgets.AbstractButtonMixin, QtWidgets.QCheckBox):
    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stateChanged.connect(self.value_changed)

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
