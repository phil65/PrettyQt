from typing import Optional, Literal

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


STATE = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

StateStr = Literal["unchecked", "partial", "checked"]

QtWidgets.QCheckBox.__bases__ = (widgets.AbstractButton,)


class CheckBox(QtWidgets.QCheckBox):

    value_changed = core.Signal(int)

    def __init__(
        self,
        label: str = "",
        parent: Optional[QtWidgets.QWidget] = None,
        checked: bool = False,
    ):
        super().__init__(label, parent)
        self.stateChanged.connect(self.value_changed)
        self.setChecked(checked)

    def __setstate__(self, state):
        self.set_id(state.get("object_name", ""))
        self.setCheckable(state["checkable"])
        self.setTristate(state.get("is_tristate", False))
        self.set_checkstate(state["checkstate"])
        self.setText(state.get("text", ""))
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bool__(self):
        return self.isChecked()

    def serialize_fields(self):
        return dict(
            checkable=self.isCheckable(),
            checkstate=self.get_checkstate(),
            is_tristate=self.isTristate(),
            text=self.text(),
        )

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)

    def set_checkstate(self, state: StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        self.setCheckState(STATE[state])

    def get_checkstate(self) -> StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return STATE.inverse[self.checkState()]

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = CheckBox("test")
    widget.show()
    app.main_loop()
