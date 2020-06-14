# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union

import qtawesome as qta
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui
from prettyqt.utils import bidict

PRIORITIES = bidict(low=QtWidgets.QAction.LowPriority,
                    normal=QtWidgets.QAction.NormalPriority,
                    high=QtWidgets.QAction.HighPriority)

CONTEXTS = bidict(widget=QtCore.Qt.WidgetShortcut,
                  widget_with_children=QtCore.Qt.WidgetWithChildrenShortcut,
                  window=QtCore.Qt.WindowShortcut,
                  application=QtCore.Qt.ApplicationShortcut)


QtWidgets.QAction.__bases__ = (core.Object,)


class Action(QtWidgets.QAction):

    def __init__(self, parent=None, text="", icon=None, shortcut="", tooltip=""):
        super().__init__(parent)
        self.set_text(text)
        self.set_icon(icon)
        self.set_shortcut(shortcut)
        self.set_tooltip(tooltip)

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    shortcut=self.shortcut(),
                    tooltip=self.toolTip(),
                    checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    priority=self.get_priority(),
                    shortcut_context=self.get_shortcut_context(),
                    statustip=self.statusTip())

    def __setstate__(self, state):
        self.__init__()
        self.set_text(state.get("text", ""))
        self.set_enabled(state.get("enabled", True))
        self.set_shortcut(state["shortcut"])
        self.set_tooltip(state.get("tooltip", ""))
        self.set_statustip(state.get("statustip", ""))
        self.set_checked(state.get("checked", False))
        self.set_priority(state["priority"])
        self.set_shortcut_context(state["shortcut_context"])
        self.set_checkable(state["checkable"])

    def set_text(self, text: str):
        self.setText(text)

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(self, text: str):
        self.setToolTip(text)

    def set_statustip(self, text: str):
        self.setStatusTip(text)

    def set_checked(self, value: bool):
        self.setChecked(value)

    def set_checkable(self, value: bool):
        self.setCheckable(value)

    def set_icon(self, icon: Union[QtGui.QIcon, str, None]):
        """set the icon for the action

        Args:
            icon: icon to use
        """
        if not icon:
            icon = gui.Icon()
        elif isinstance(icon, str):
            icon = qta.icon(icon)
        self.setIcon(icon)

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)

    def set_menu(self, menu):
        self.setMenu(menu)

    def set_priority(self, priority: str):
        """set priority of the action

        Allowed values are "low", "normal", "high"

        Args:
            mode: priority for the action

        Raises:
            ValueError: priority does not exist
        """
        if priority not in PRIORITIES:
            raise ValueError(f"{priority} not a valid priority.")
        self.setPriority(PRIORITIES[priority])

    def get_priority(self) -> str:
        """returns current priority

        Possible values: "low", "normal", "high"

        Returns:
            priority
        """
        return PRIORITIES.inv[self.priority()]

    def set_shortcut_context(self, context: str):
        """set shortcut context

        Allowed values are "widget", "widget_with_children", "window", "application"

        Args:
            mode: shortcut context

        Raises:
            ValueError: shortcut context does not exist
        """
        if context not in CONTEXTS:
            raise ValueError(f"{context} not a valid shortcut context.")
        self.setShortcutContext(CONTEXTS[context])

    def get_shortcut_context(self) -> str:
        """returns shortcut context

        Possible values: "widget", "widget_with_children", "window", "application"

        Returns:
            shortcut context
        """
        return CONTEXTS.inv[self.shortcutContext()]

    def show_shortcut_in_contextmenu(self, state: bool = True):
        self.setShortcutVisibleInContextMenu(state)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    action = Action("This is a test")
    print(action.__getstate__())
    app.exec_()
