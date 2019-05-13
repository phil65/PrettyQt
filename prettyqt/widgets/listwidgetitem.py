# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets, QtCore

from prettyqt import gui


STATES = bidict(dict(unchecked=QtCore.Qt.Unchecked,
                     partial=QtCore.Qt.PartiallyChecked,
                     checked=QtCore.Qt.Checked))


class ListWidgetItem(QtWidgets.QListWidgetItem):

    def __repr__(self):
        return f"ListWidgetItem({self.icon()}, {repr(self.text())})"

    def __getstate__(self):
        return dict(text=self.text(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    checkstate=self.get_checkstate(),
                    icon=gui.Icon(self.icon()),
                    data=self.data(QtCore.Qt.UserRole))

    def __setstate__(self, state):
        self.__init__()
        self.setText(state["text"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])
        self.setData(QtCore.Qt.UserRole, state["data"])
        self.setIcon(state["icon"])
        self.set_checkstate(state["checkstate"])

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
