# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets, QtCore


PRIORITIES = dict(low=QtWidgets.QAction.LowPriority,
                  normal=QtWidgets.QAction.NormalPriority,
                  high=QtWidgets.QAction.HighPriority)

CONTEXTS = dict(widget=QtCore.Qt.WidgetShortcut,
                widget_with_children=QtCore.Qt.WidgetWithChildrenShortcut,
                window=QtCore.Qt.WindowShortcut,
                application=QtCore.Qt.ApplicationShortcut)


class Action(QtWidgets.QAction):

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    shortcut=self.shortcut(),
                    tooltip=self.toolTip(),
                    checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    priority=self.priority(),
                    shortcut_context=self.shortcutContext(),
                    statustip=self.statusTip())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state["text"])
        self.setEnabled(state["enabled"])
        self.set_shortcut(state["shortcut"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])
        self.setChecked(state["checked"])
        self.setPriority(state["priority"])
        self.setShortcutContext(state["shortcut_context"])
        self.setCheckable(state["checkable"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(self, text: str):
        self.setToolTip(text)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)

    def set_priority(self, priority: str):
        if priority not in PRIORITIES:
            raise ValueError(f"{priority} not a valid priority.")
        self.setPriority(PRIORITIES[priority])

    def set_shortcut_context(self, context: str):
        if context not in CONTEXTS:
            raise ValueError(f"{context} not a valid shortcut context.")
        self.setShortcutContext(CONTEXTS[context])


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    action = Action("This is a test")
    print(action.__getstate__())
    app.exec_()
