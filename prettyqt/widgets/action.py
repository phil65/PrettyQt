# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets


class Action(QtWidgets.QAction):

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    shortcut=self.shortcut(),
                    tooltip=self.toolTip())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state["text"])
        self.setEnabled(state["enabled"])
        self.set_shortcut(state["shortcut"])
        self.setToolTip(state["tooltip"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(self, text):
        self.setToolTip(text)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)
