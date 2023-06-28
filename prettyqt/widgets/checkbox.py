from __future__ import annotations

from prettyqt import constants, core, widgets


class CheckBox(widgets.AbstractButtonMixin, widgets.QCheckBox):
    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stateChanged.connect(self.value_changed)

    def set_checkstate(self, state: constants.CheckStateStr | constants.CheckState):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use
        """
        self.setCheckState(constants.CHECK_STATE.get_enum_value(state))

    def get_checkstate(self) -> constants.CheckStateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.CHECK_STATE.inverse[self.checkState()]


if __name__ == "__main__":
    app = widgets.app()
    widget = CheckBox("test")
    widget.show()
    app.exec()
