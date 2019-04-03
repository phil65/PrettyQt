# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable, Optional, Any

from qtpy import QtWidgets, QtCore
from prettyqt import widgets

import qtawesome as qta


class Menu(QtWidgets.QMenu):

    def __init__(self, title="", icon=None, parent=None):
        super().__init__(title, parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def set_icon(self, icon):
        """set the icon for the menu

        Args:
            icon: icon to use
        """
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def _separator(self, text: str) -> QtWidgets.QWidgetAction:
        """returns a separator showing a label

        Args:
            text: Text to show on separator

        Returns:
            Separator widget
        """
        label = QtWidgets.QLabel(text)
        label.setMinimumWidth(self.minimumWidth())
        label.setStyleSheet("background:lightgrey")
        label.setAlignment(QtCore.Qt.AlignCenter)
        separator = QtWidgets.QWidgetAction(self)
        separator.setDefaultWidget(label)
        return separator

    def add_action(self,
                   label: str,
                   callback: Callable,
                   icon: Optional[Any] = None,
                   checkable: bool = False,
                   checked: bool = False,
                   shortcut: Optional[str] = None,
                   status_tip: Optional[str] = None
                   ) -> QtWidgets.QAction:
        """Add an action to the menu

        Args:
            label: Label for button
            callback: gets called when action is triggered
            icon: icon for button (default: {None})
            checkable: as checkbox button (default: {False})
            checked: if checkable, turn on by default (default: {False})
            shortcut: Shortcut for action (a) (default: {None})
            status_tip: Status tip to be shown in status bar (default: {None})

        Returns:
            Action added to menu
        """
        action = widgets.Action(label, parent=self)
        action.triggered.connect(callback)
        action.set_icon(icon)
        action.set_shortcut(shortcut)
        if checkable:
            action.setCheckable(True)
            action.setChecked(checked)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        self.addAction(action)
        return action
