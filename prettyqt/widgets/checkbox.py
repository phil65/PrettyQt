# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)


QtWidgets.QCheckBox.__bases__ = (widgets.AbstractButton,)


class CheckBox(QtWidgets.QCheckBox):

    value_changed = core.Signal(int)

    def __init__(self, label="", parent=None, checked=False):
        super().__init__(label, parent)
        self.stateChanged.connect(self.value_changed)
        self.setChecked(checked)

    def __getstate__(self):
        return dict(
            object_name=self.id,
            checkable=self.isCheckable(),
            checkstate=self.get_checkstate(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
            is_tristate=self.isTristate(),
            text=self.text(),
            enabled=self.isEnabled(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_id(state.get("object_name", ""))
        self.setCheckable(state["checkable"])
        self.setTristate(state.get("is_tristate", False))
        self.set_checkstate(state["checkstate"])
        self.setText(state.get("text", ""))
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

    def __bool__(self):
        return self.isChecked()

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)

    def set_checkstate(self, state: str):
        """set checkstate of the checkbox

        valid values are: unchecked, partial, checked

        Args:
            state: checkstate to use

        Raises:
            ValueError: invalid checkstate
        """
        if state not in STATES:
            raise ValueError("Invalid checkstate.")
        self.setCheckState(STATES[state])

    def get_checkstate(self) -> bool:
        """returns checkstate

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
