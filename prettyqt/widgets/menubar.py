from __future__ import annotations

import functools
from typing import Literal, overload

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtGui, QtWidgets


class MenuBar(widgets.WidgetMixin, QtWidgets.QMenuBar):
    def __add__(self, other: QtGui.QAction | QtWidgets.QMenu):
        self.add(other)
        return self

    def serialize_fields(self):
        return dict(
            default_up=self.isDefaultUp(),
            native_menu_bar=self.isNativeMenuBar(),
        )

    @overload
    def add_menu(self, menu_or_str: str) -> widgets.Menu:
        ...

    @overload
    def add_menu(self, menu_or_str: QtWidgets.QMenu) -> gui.Action:
        ...

    @functools.singledispatchmethod
    def add_menu(self, title: str) -> widgets.Menu:
        action = gui.Action(parent=self, text=title)
        menu = widgets.Menu(title=title, parent=self)
        action.set_menu(menu)
        self.addAction(action)
        return menu

    @add_menu.register
    def _(self, menu: QtWidgets.QMenu) -> gui.Action:
        action = gui.Action(parent=self, text=menu.title())
        action.set_menu(menu)
        self.addAction(action)
        return action

    def add_separator(self):
        self.addSeparator()

    def add(self, *items: QtWidgets.QMenu | QtGui.QAction):
        for i in items:
            if isinstance(i, QtWidgets.QMenu):
                action = gui.Action(self)
                action.set_text(i.title())
                action.set_menu(i)
                self.addAction(action)
            else:
                self.addAction(i)

    def set_corner_widget(
        self,
        widget: QtWidgets.QWidget,
        corner: Literal["top_right", "top_left"] = "top_right",
    ):
        match corner:
            case "top_left":
                self.setCornerWidget(widget, constants.Corner.TopLeftCorner)
            case "top_right":
                self.setCornerWidget(widget, constants.Corner.TopRightCorner)
            case _:
                raise ValueError(corner)

    def get_corner_widget(
        self,
        corner: Literal["top_right", "top_left"] = "top_right",
    ) -> QtWidgets.QWidget:
        match corner:
            case "top_left":
                return self.cornerWidget(constants.Corner.TopLeftCorner)
            case "top_right":
                return self.cornerWidget(constants.Corner.TopRightCorner)
            case _:
                raise ValueError(corner)


if __name__ == "__main__":
    app = widgets.app()
    win = widgets.MainWindow()
    menu_bar = MenuBar()
    menuaction = menu_bar.add_menu("test")
    act = menu_bar.add_action("action")
    sep = menu_bar.addSeparator()
    act2 = menu_bar.add_action("action2")
    menu = widgets.Menu("testaa")
    menu_bar.add(menu)
    win.setMenuBar(menu_bar)
    win.show()
    app.exec()
