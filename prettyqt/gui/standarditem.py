# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class StandardItem(QtGui.QStandardItem):

    def __repr__(self):
        return f"StandardItem({self.icon()}, {self.text()!r})"

    def __getstate__(self):
        return dict(text=self.text(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    icon=gui.Icon(self.icon()),
                    data=self.data())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setData(state["data"])
        self.setIcon(state["icon"])
