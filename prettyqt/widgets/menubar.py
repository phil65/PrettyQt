from typing import Literal, overload

from prettyqt import constants, gui, widgets


class MenuBar(widgets.WidgetMixin, widgets.QMenuBar):
    """Horizontal menu bar."""

    def __add__(self, other: gui.QAction | widgets.QMenu):
        self.add(other)
        return self

    def serialize_fields(self):
        return dict(
            default_up=self.isDefaultUp(),
            native_menu_bar=self.isNativeMenuBar(),
        )

    @overload
    def add_menu(self, menu_or_str: str) -> widgets.Menu: ...

    @overload
    def add_menu(self, menu_or_str: widgets.QMenu) -> gui.Action: ...

    def add_menu(self, menu_or_str: str | widgets.QMenu) -> widgets.Menu | gui.Action:
        if isinstance(menu_or_str, str):
            action = gui.Action(parent=self, text=menu_or_str)
            menu = widgets.Menu(title=menu_or_str, parent=self)
            action.set_menu(menu)
            self.addAction(action)
            return menu
        action = gui.Action(parent=self, text=menu_or_str.title())
        action.set_menu(menu_or_str)
        self.addAction(action)
        return action

    def add_separator(self):
        self.addSeparator()

    def add(self, *items: widgets.QMenu | gui.QAction):
        for i in items:
            if isinstance(i, widgets.QMenu):
                action = gui.Action(self)
                action.set_text(i.title())
                action.set_menu(i)
                self.addAction(action)
            else:
                self.addAction(i)

    def set_corner_widget(
        self,
        widget: widgets.QWidget,
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
    ) -> widgets.QWidget:
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
