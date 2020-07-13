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


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return "TreeWidgetItem()"

    def __getstate__(self):
        icon = self.icon(0)
        return dict(
            text=self.text(0),
            tooltip=self.toolTip(0),
            statustip=self.statusTip(0),
            checkstate=self.get_checkstate(),
            icon=gui.Icon(icon) if not icon.isNull() else None,
            data=self.data(0, QtCore.Qt.UserRole),
        )

    def __setstate__(self, state):
        self.__init__()
        self.setText(0, state.get("text", ""))
        self.setToolTip(0, state.get("tooltip", ""))
        self.setStatusTip(0, state.get("statustip", ""))
        self.setData(0, QtCore.Qt.UserRole, state["data"])
        self.set_icon(state["icon"])
        self.set_checkstate(state["checkstate"])

    def set_icon(self, icon: gui.icon.IconType):
        """set the icon for the action

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(0, icon)

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
        self.setCheckState(0, STATES[state])

    def get_checkstate(self) -> str:
        """returns checkstate

        possible values are "unchecked", "partial", "checked"

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState(0)]
