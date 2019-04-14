# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets


class ToolButton(QtWidgets.QToolButton):

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
