# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtGui

from prettyqt import core, gui


class StandardItem(QtGui.QStandardItem):
    def __repr__(self):
        return f"StandardItem({self.icon()}, {self.text()!r})"

    def __getstate__(self):
        return dict(
            text=self.text(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            data=self.data(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setData(state["data"])
        self.set_icon(state["icon"])

    def clone(self):
        item = self.__class__()
        ba = QtCore.QByteArray()
        ds = QtCore.QDataStream(ba, core.IODevice.WriteOnly)
        ds << self
        ds = QtCore.QDataStream(ba)
        ds >> item
        assert type(item) == StandardItem
        return item

    def set_icon(self, icon: gui.icon.IconType):
        """set the icon for the action

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)
