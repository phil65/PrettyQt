from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Callable

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


QtWidgets.QMenu.__bases__ = (widgets.Widget,)


class Menu(QtWidgets.QMenu):
    def __init__(
        self,
        title: str = "",
        icon: types.IconType = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(title, parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def __iter__(self) -> Iterator[QtWidgets.QAction]:
        return iter(self.actions())

    def __len__(self) -> int:
        return len(self.actions())

    def __add__(self, other: QtWidgets.QAction):
        self.add(other)
        return self

    def __getitem__(self, item: str) -> QtWidgets.QAction:
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

    def add(self, *item: QtWidgets.QAction):
        for i in item:
            i.setParent(self)
            self.addAction(i)

    def set_icon(self, icon: types.IconType):
        """Set the icon for the menu.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        if icon.isNull():
            return None
        return gui.Icon(icon)

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

    def add_action(
        self,
        label: str | widgets.Action,
        callback: Callable = None,
        icon: Any | None = None,
        checkable: bool = False,
        checked: bool = False,
        shortcut: str | None = None,
        status_tip: str | None = None,
    ) -> widgets.Action:
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
        if isinstance(label, str):
            action = widgets.Action(text=label, parent=self)
            if callback:
                action.triggered.connect(callback)
            action.set_icon(icon)
            action.set_shortcut(shortcut)
            if checkable:
                action.setCheckable(True)
                action.setChecked(checked)
            if status_tip is not None:
                action.setStatusTip(status_tip)
        else:
            action = label
            action.setParent(self)
        self.addAction(action)
        return action

    def add_actions(self, actions: list[QtWidgets.QAction]):
        self.addActions(actions)

    def add_menu(self, menu: QtWidgets.QMenu) -> QtWidgets.QAction:
        action = menu.menuAction()
        self.addAction(action)
        return action


if __name__ == "__main__":
    app = widgets.app()
    menu = Menu("1")
    action = widgets.Action(text="test")
    menu.addAction(action)
    menu.show()
    menu.exec_(core.Point(200, 200))
