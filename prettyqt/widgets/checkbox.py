# -*- coding: utf-8 -*-

from typing import Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)


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

    def serialize_fields(self):
        return dict(
            checkable=self.isCheckable(),
            checkstate=self.get_checkstate(),
            is_tristate=self.isTristate(),
            text=self.text(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_id(state.get("object_name", ""))
        self.setCheckable(state["checkable"])
        self.setTristate(state.get("is_tristate", False))
        self.set_checkstate(state["checkstate"])
        self.setText(state.get("text", ""))
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __bool__(self):
        return self.isChecked()

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)

    def set_checkstate(self, state: str):
        """Set checkstate of the checkbox.

        valid values are: unchecked, partial, checked

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATES:
            raise InvalidParamError(state, STATES)
        self.setCheckState(STATES[state])

    def get_checkstate(self) -> bool:
        """Return checkstate.

        possible values are "unchecked", "partial", "checked"

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState()]

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = CheckBox("test")
    widget.show()
    app.exec_()
