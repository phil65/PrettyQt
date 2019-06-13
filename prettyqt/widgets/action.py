# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union

import qtawesome as qta
from qtpy import QtCore, QtWidgets, QtGui

from prettyqt import gui, core
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
        self.setText(state.get("text", ""))
        self.setEnabled(state.get("enabled", True))
        self.set_shortcut(state["shortcut"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setChecked(state.get("checked", False))
        self.set_priority(state["priority"])
        self.set_shortcut_context(state["shortcut_context"])
        self.setCheckable(state["checkable"])

    def set_text(self, text: str):
        self.setText(text)

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(self, text: str):
        self.setToolTip(text)

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


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    action = Action("This is a test")
    print(action.__getstate__())
    app.exec_()
