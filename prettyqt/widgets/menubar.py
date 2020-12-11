from typing import Union, overload

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QMenuBar.__bases__ = (widgets.Widget,)


class MenuBar(QtWidgets.QMenuBar):
    def __add__(self, other):
        if isinstance(other, (QtWidgets.QAction, QtWidgets.QMenu)):
            self.add(other)
            return self

    def serialize_fields(self):
        return dict(
            default_up=self.isDefaultUp(),
            native_menu_bar=self.isNativeMenuBar(),
        )

    def add_action(self, action: Union[QtWidgets.QAction, str]) -> QtWidgets.QAction:
        if isinstance(action, str):
            action = widgets.Action(parent=self, text=action)
            self.addAction(action)
            return action
        return self.addAction(action)

    @overload
    def add_menu(self, menu_or_str: str) -> widgets.Menu:
        ...

    @overload
    def add_menu(self, menu_or_str: QtWidgets.QMenu) -> widgets.Action:
        ...

    def add_menu(self, menu_or_str):
        action = widgets.Action(parent=self)
        if isinstance(menu_or_str, str):
            menu = widgets.Menu(menu_or_str)
            action.set_text(menu_or_str)
            action.setMenu(menu)
            self.addAction(action)
            return menu
        else:
            action.setMenu(menu_or_str)
            action.set_text(menu_or_str.title())
            self.addAction(action)
            return action

    def add_separator(self):
        self.addSeparator()

    def add(self, *items: Union[QtWidgets.QMenu, QtWidgets.QAction]):
        for i in items:
            if isinstance(i, QtWidgets.QMenu):
                action = widgets.Action(parent=self)
                action.set_text(i.title())
                action.setMenu(i)
                self.addAction(action)
            else:
                self.addAction(i)


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
    app.main_loop()
