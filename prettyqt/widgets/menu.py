from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core, gui, iconprovider, widgets


if TYPE_CHECKING:
    from collections.abc import Iterator

    from prettyqt.utils import datatypes


class MenuMixin(widgets.WidgetMixin):
    def __init__(self, *args, tool_tips_visible=True, **kwargs):
        super().__init__(*args, tool_tips_visible=tool_tips_visible, **kwargs)

    def __iter__(self) -> Iterator[gui.QAction]:
        return iter(self.actions())

    def __len__(self) -> int:
        return len(self.actions())

    def __add__(self, other: gui.QAction):
        self.add(other)
        return self

    def __getitem__(self, item: str) -> gui.QAction:
        for action in self.actions():
            if action.objectName() == item:
                return action
        msg = f"Action {item} not in menu"
        raise KeyError(msg)

    def add(self, *item: gui.QAction):
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
        separator = widgets.WidgetAction(self)
        if text is None:
            separator.setSeparator(True)
        else:
            label = widgets.Label(
                text, minimum_width=self.minimumWidth(), alignment="center"
            )
            with label.edit_stylesheet() as ss:
                ss.background.setValue("lightgrey")
            separator.setDefaultWidget(label)
            separator.setEnabled(False)
        self.add(separator)
        return separator

    def add_menu(self, menu: widgets.QMenu) -> gui.Action:
        action = gui.Action(text=menu.title(), icon=menu.icon())
        action.setMenu(menu)
        super().addAction(action)
        return action


class Menu(MenuMixin, widgets.QMenu):
    """Menu widget for use in menu bars, context menus, and other popup menus."""


if __name__ == "__main__":
    app = widgets.app()
    menu = Menu("1")
    action = gui.Action(text="test")
    menu.addAction(action)
    menu.show()
    menu.exec(core.Point(200, 200))
