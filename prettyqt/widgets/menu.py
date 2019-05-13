# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Any, Callable, Optional

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import core, widgets


class Menu(QtWidgets.QMenu):

    def __init__(self, title="", icon=None, parent=None):
        super().__init__(title, parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def __iter__(self):
        return iter(self.actions())

    def __add__(self, other):
        if isinstance(other, QtWidgets.QAction):
            self.addAction(other)
            return self

    def set_icon(self, icon):
        """set the icon for the menu

        Args:
            icon: icon to use
        """
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def _separator(self, text: str) -> widgets.WidgetAction:
        """returns a separator showing a label

        Args:
            text: Text to show on separator

        Returns:
            Separator widget
        """
        label = widgets.Label(text)
        label.setMinimumWidth(self.minimumWidth())
        label.setStyleSheet("background:lightgrey")
        label.set_alignment(horizontal="center")
        separator = widgets.WidgetAction(self)
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
                   ) -> widgets.Action:
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


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    menu = Menu("1")
    action = widgets.Action("test")
    menu.addAction(action)
    menu.show()
    menu.exec_(core.Point(200, 200))
