from typing import Any, Callable, Iterator, List, Optional, Union

from qtpy import QtWidgets

from prettyqt import core, gui, widgets


QtWidgets.QMenu.__bases__ = (widgets.Widget,)


class Menu(QtWidgets.QMenu):
    def __init__(
        self,
        title: str = "",
        icon: gui.icon.IconType = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(title, parent=parent)
        self.set_icon(icon)
        self.setToolTipsVisible(True)

    def __iter__(self) -> Iterator[QtWidgets.QAction]:
        return iter(self.actions())

    def __len__(self) -> int:
        return len(self.actions())

    def __add__(self, other):
        if isinstance(other, QtWidgets.QAction):
            self.add(other)
            return self
        raise TypeError("Invalid Type")

    def __getitem__(self, item: str) -> QtWidgets.QAction:
        for action in self.actions():
            if action.objectName() == item:
                return action
        raise KeyError(f"Action {item} not in menu")

    def add(self, *item: QtWidgets.QAction):
        for i in item:
            i.setParent(self)
            self.addAction(i)

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the menu.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def add_separator(self, text: Optional[str] = None) -> widgets.WidgetAction:
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
        label: Union[str, widgets.Action],
        callback: Callable = None,
        icon: Optional[Any] = None,
        checkable: bool = False,
        checked: bool = False,
        shortcut: Optional[str] = None,
        status_tip: Optional[str] = None,
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

    def add_actions(self, actions: List[QtWidgets.QAction]):
        self.addActions(actions)

    def add_menu(self, menu: QtWidgets.QMenu) -> QtWidgets.QAction:
        return self.addAction(menu.menuAction())


if __name__ == "__main__":
    app = widgets.app()
    menu = Menu("1")
    action = widgets.Action(text="test")
    menu.addAction(action)
    menu.show()
    menu.exec_(core.Point(200, 200))
