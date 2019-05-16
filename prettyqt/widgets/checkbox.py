# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets, QtCore
from prettyqt import core, widgets

STATES = bidict(dict(unchecked=QtCore.Qt.Unchecked,
                     partial=QtCore.Qt.PartiallyChecked,
                     checked=QtCore.Qt.Checked))


class CheckBox(QtWidgets.QCheckBox):

    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stateChanged.connect(self.value_changed)

    def __getstate__(self):
        return dict(object_name=self.objectName(),
                    checkable=self.isCheckable(),
                    checkstate=self.get_checkstate(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    is_tristate=self.isTristate(),
                    text=self.text(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        self.setObjectName(state.get("object_name", ""))
        self.setCheckable(state["checkable"])
        self.setTristate(state.get("is_tristate", False))
        self.set_checkstate(state["checkstate"])
        self.setText(state.get("text", ""))
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

    def __bool__(self):
        return self.isChecked()

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

    def get_checkstate(self):
        return STATES.inv[self.checkState()]

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)


CheckBox.__bases__[0].__bases__ = (widgets.AbstractButton,)


if __name__ == "__main__":
    app = widgets.app()
    widget = CheckBox("test")
    widget.show()
    app.exec_()
