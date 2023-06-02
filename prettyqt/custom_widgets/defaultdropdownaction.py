from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtGui


class DefaultDropDownAction(widgets.WidgetAction):
    """This action provides a button as well as a dropdown to choose a default action.

    The default action can be selected from a drop down list. The last one used
    becomes the default one.

    The default action is directly usable without using the drop down list.
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        button = widgets.ToolButton(parent)
        button.set_popup_mode("menu_button")
        self.setDefaultWidget(button)
        self._button = button

    def get_menu(self) -> widgets.Menu:
        """Returns the menu."""
        menu = self._button.menu()
        if menu is None:
            menu = widgets.Menu(self._button)
            self._button.setMenu(menu)
        return menu

    def addAction(self, action: QtGui.QAction):
        """Add a new action to the list."""
        menu = self.get_menu()
        menu.addAction(action)
        if self._button.defaultAction() is None:
            self._button.setDefaultAction(action)
        if action.isCheckable():
            action.toggled.connect(self._toggled)

    def _toggled(self, checked: bool):
        if checked:
            action = self.sender()
            self._button.setDefaultAction(action)


if __name__ == "__main__":
    from prettyqt import gui

    app = widgets.app()
    window = widgets.MainWindow()
    toolbar = widgets.ToolBar()
    action = gui.Action("test")
    window.add_toolbar(toolbar, "top")
    widgetaction = DefaultDropDownAction()
    widgetaction.addAction(action)
    toolbar.addAction(widgetaction)
    window.show()
    app.main_loop()
