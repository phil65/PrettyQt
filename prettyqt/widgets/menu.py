# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta


class Menu(QtWidgets.QMenu):

    def __init__(self, icon=None, parent=None):
        super().__init__(parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def _separator(self, text: str) -> QtWidgets.QWidgetAction:
        label = QtWidgets.QLabel(text)
        label.setMinimumWidth(self.minimumWidth())
        label.setStyleSheet("background:lightgrey")
        label.setAlignment(QtCore.Qt.AlignCenter)
        separator = QtWidgets.QWidgetAction(self)
        separator.setDefaultWidget(label)
        return separator

    def add_action(self, label, callback, icon=None, checkable=False, shortcut=None):
        action = QtWidgets.QAction(label, parent=self)
        action.triggered.connect(callback)
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            action.setIcon(icon)
        if shortcut:
            action.setShortcut(shortcut)
        action.setCheckable(checkable)
        self.addAction(action)
        return action
