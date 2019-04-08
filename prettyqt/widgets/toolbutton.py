# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
import qtawesome as qta


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
    def for_menu(cls, menu):
        btn = cls()
        btn.setMenu(menu)
        btn.setPopupMode(cls.InstantPopup)
        return btn
