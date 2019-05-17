# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union

import qtawesome as qta
from qtpy import QtGui

from prettyqt import gui


class StandardItem(QtGui.QStandardItem):

    def __repr__(self):
        return f"StandardItem({self.icon()}, {self.text()!r})"

    def __getstate__(self):
        return dict(text=self.text(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
                    data=self.data())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setData(state["data"])
        self.set_icon(state["icon"])

    def set_icon(self, icon: Union[QtGui.QIcon, str, None]):
        """set the icon for the action

        Args:
            icon: icon to use
        """
        if icon is None:
            icon = gui.Icon()
        elif isinstance(icon, str):
            icon = qta.icon(icon)
        self.setIcon(icon)
