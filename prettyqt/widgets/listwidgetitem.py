# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import gui
from prettyqt.utils import bidict


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)


class ListWidgetItem(QtWidgets.QListWidgetItem):
    def __repr__(self):
        return f"ListWidgetItem({self.icon()}, {self.text()!r})"

    def __getstate__(self):
        return dict(
            text=self.text(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
            checkstate=self.get_checkstate(),
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            data=self.data(QtCore.Qt.UserRole),
        )

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setData(QtCore.Qt.UserRole, state["data"])
        self.set_icon(state["icon"])
        self.set_checkstate(state["checkstate"])

    def set_icon(self, icon: gui.icon.IconType):
        """set the icon for the action

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

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

    def get_checkstate(self) -> str:
        """returns checkstate

        possible values are "unchecked", "partial", "checked"

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState()]
