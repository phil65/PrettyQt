# -*- coding: utf-8 -*-
"""
"""

from typing import Callable, Optional, Union, Dict

from qtpy import QtWidgets, QtCore

from prettyqt import gui, widgets


class SidebarWidget(widgets.MainWindow):
    BUTTON_WIDTH = 100
    SETTINGS_BUTTON_HEIGHT = 28

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        show_settings: bool = False,
        main_layout: Union[str, QtWidgets.QLayout] = "vertical",
    ):
        super().__init__(parent=parent)
        self.button_map: Dict[QtWidgets.QWidget, QtWidgets.QToolButton] = dict()
        self.sidebar = widgets.ToolBar()
        self.sidebar.set_id("SidebarWidget")
        self.sidebar.set_title("Sidebar")
        self.sidebar.set_style("text_below_icon")
        self.sidebar.set_contextmenu_policy("prevent")
        self.sidebar.setFloatable(False)
        self.sidebar.set_allowed_areas("all")
        self.settings_menu = widgets.Menu()
        self.sidebar.set_icon_size(60)
        if show_settings:
            self.settings_btn = self.sidebar.add_menu_button(
                "", icon="mdi.settings", menu=self.settings_menu
            )
            self.settings_btn.setFixedWidth(self.BUTTON_WIDTH)
            self.settings_btn.setFixedHeight(self.SETTINGS_BUTTON_HEIGHT)
            self.settings_btn.set_style("icon")
            self.sidebar.orientationChanged.connect(self.on_orientation_change)
            self.sidebar.add_separator()
        self.spacer_action = self.sidebar.add_spacer()
        self.add_toolbar(self.sidebar, "left")
        self.area = widgets.Widget()
        self.area.set_layout("stacked")
        w = widgets.Widget()
        w.set_layout(main_layout)
        self.main_layout = w.box
        self.main_layout.set_margin(0)
        self.main_layout += self.area
        self.setCentralWidget(w)

    def on_orientation_change(self, orientation: QtCore.Qt.Orientation):
        if orientation == QtCore.Qt.Horizontal:
            self.settings_btn.setFixedWidth(34)
            self.settings_btn.setFixedHeight(34)
        else:
            self.settings_btn.setFixedWidth(self.BUTTON_WIDTH)
            self.settings_btn.setFixedHeight(self.SETTINGS_BUTTON_HEIGHT)

    def add_tab(
        self,
        item: QtWidgets.QWidget,
        title: str,
        icon: gui.icon.IconType = None,
        show: bool = False,
        shortcut: Optional[str] = None,
        area: str = "top",
    ):
        self.area.box.add(item)
        # button = widgets.ToolButton()
        # button.set_text(title)
        # button.set_icon_size(40)
        # button.setFixedSize(80, 80)
        # button.set_icon(icon)
        # button.clicked.connect(lambda: self.area.box.setCurrentWidget(item))
        # self.sidebar.addWidget(button)
        # self.sidebar.add_separator()
        if area == "top":
            act = widgets.Action(
                text=title, icon=icon, shortcut=shortcut, parent=self.sidebar
            )
            act.setCheckable(True)
            act.triggered.connect(lambda: self.set_tab(item))
            self.sidebar.insertAction(self.spacer_action, act)
        else:
            act = self.sidebar.add_action(
                title, icon, lambda: self.set_tab(item), checkable=True
            )
        button = self.sidebar.widgetForAction(act)
        button.setFixedWidth(self.BUTTON_WIDTH)
        if len(self.area.box) == 1:
            button.setChecked(True)
        self.button_map[item] = button
        if show:
            self.area.box.setCurrentWidget(item)

    def set_tab(self, item: Union[str, int, widgets.Widget]):
        if isinstance(item, int):
            item = self.area.box[item]
        elif isinstance(item, str):
            item = self.find_child(QtWidgets.QWidget, name=item, recursive=False)
        if item not in self.area.box:
            raise ValueError("Layout does not contain the chosen widget")
        current = self.area.box.currentWidget()
        self.button_map[current].setChecked(False)
        self.area.box.setCurrentWidget(item)
        self.button_map[item].setChecked(True)

    def show_tab(self, index):
        widget = self.area.box[index]
        self.area.box.setCurrentWidget(widget)

    def add_spacer(self) -> widgets.Widget:
        return self.sidebar.add_spacer()

    def add_separator(self, text: Optional[str] = None, area: str = "top"):
        if area == "top":
            self.sidebar.add_separator(text, before=self.spacer_action)
        else:
            self.sidebar.add_separator(text)

    def add_action(
        self,
        title: str,
        icon: gui.icon.IconType = None,
        callback: Callable = None,
        checkable: bool = False,
        shortcut: Optional[str] = None,
        area: str = "top",
    ):
        # act = self.sidebar.add_action(label=title,
        #                                      icon=icon,
        #                                      callback=callback,
        #                                      checkable=checkable)
        act = widgets.Action(text=title, icon=icon, shortcut=shortcut)
        act.setCheckable(checkable)
        if callback:
            act.triggered.connect(callback)
        if area == "top":
            self.sidebar.insertAction(self.spacer_action, act)
        if area == "bottom":
            self.sidebar.addAction(act)
        button = self.sidebar.widgetForAction(act)
        button.setFixedWidth(self.BUTTON_WIDTH)
        return act


if __name__ == "__main__":
    app = widgets.app()
    ex = SidebarWidget(show_settings=True)
    page_1 = widgets.PlainTextEdit()
    page_2 = widgets.ColorDialog()
    page_3 = widgets.FileDialog()
    ex.add_tab(page_1, "Text", "mdi.timer")
    ex.add_tab(page_2, "Color", "mdi.format-color-fill", area="bottom")
    ex.add_tab(page_3, "Help", "mdi.help-circle-outline")
    # ex.show_tab(0)
    ex.show()
    app.exec_()
