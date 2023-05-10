from __future__ import annotations

from collections.abc import Callable, Iterator
import functools
from typing import Any

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import datatypes


class MenuMixin(widgets.WidgetMixin):
    def __init__(
        self,
        title: str = "",
        icon: datatypes.IconType = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(title, parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def __iter__(self) -> Iterator[QtGui.QAction]:
        return iter(self.actions())

    def __len__(self) -> int:
        return len(self.actions())

    def __add__(self, other: QtGui.QAction):
        self.add(other)
        return self

    def __getitem__(self, item: str) -> QtGui.QAction:
        for action in self.actions():
            if action.objectName() == item:
                return action
        raise KeyError(f"Action {item} not in menu")

    def serialize_fields(self):
        return dict(
            separators_collapsible=self.separatorsCollapsible(),
            tearoff_enabled=self.isTearOffEnabled(),
            title=self.title(),
            tool_tips_visible=self.toolTipsVisible(),
            icon=self.get_icon(),
        )

    def add(self, *item: QtGui.QAction):
        for i in item:
            i.setParent(self)
            self.addAction(i)

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the menu.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def add_separator(self, text: str | None = None) -> widgets.WidgetAction:
        """Adds a separator showing an optional label.

        Args:
            text: Text to show on separator

        Returns:
            Separator action
        """
        separator = widgets.WidgetAction(parent=self)
        if text is None:
            separator.setSeparator(True)
        else:
            label = widgets.Label(text)
            label.setMinimumWidth(self.minimumWidth())
            with label.edit_stylesheet() as ss:
                ss.background.setValue("lightgrey")
            label.set_alignment(horizontal="center")
            separator.setDefaultWidget(label)
            separator.setEnabled(False)
        self.add(separator)
        return separator

    @functools.singledispatchmethod
    def add_action(self, item: QtGui.QAction):
        item.setParent(self)
        self.addAction(item)

    @add_action.register
    def _(
        self,
        label: str,
        callback: Callable = None,
        icon: Any | None = None,
        checkable: bool = False,
        checked: bool = False,
        shortcut: str | None = None,
        status_tip: str | None = None,
    ) -> gui.Action:
        """Add an action to the menu.

        Args:
            label: Label for button
            callback: gets called when action is triggered
            icon: icon for button
            checkable: as checkbox button
            checked: if checkable, turn on by default
            shortcut: Shortcut for action
            status_tip: Status tip to be shown in status bar

        Returns:
            Action added to menu
        """
        action = gui.Action(text=label, parent=self)
        if callback:
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

    def add_actions(self, actions: list[QtGui.QAction]):
        for i in actions:
            i.setParent(self)
        self.addActions(actions)

    def add_menu(self, menu: QtWidgets.QMenu) -> QtGui.QAction:
        action = menu.menuAction()
        self.addAction(action)
        return action


class Menu(MenuMixin, QtWidgets.QMenu):
    pass


if __name__ == "__main__":
    app = widgets.app()
    menu = Menu("1")
    action = gui.Action(text="test")
    menu.addAction(action)
    menu.show()
    menu.exec(core.Point(200, 200))
