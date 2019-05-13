# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import gui


class ToolButton(QtWidgets.QToolButton):

    def __getstate__(self):
        return dict(text=self.text(),
                    icon=gui.Icon(self.icon()),
                    checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state["text"])
        self.set_icon(state["icon"])
        self.setEnabled(state["enabled"])
        self.setChecked(state["checked"])
        self.setCheckable(state["checkable"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)

    @classmethod
    def for_menu(cls, menu, icon=None):
        btn = cls()
        btn.setMenu(menu)
        btn.setPopupMode(cls.InstantPopup)
        btn.set_icon(icon)
        return btn
