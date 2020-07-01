# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable, Optional, Union

from prettyqt import widgets
from prettyqt.utils import icons


class SidebarWidget(widgets.MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.sidebar = widgets.ToolBar()
        self.sidebar.id = "SidebarWidget"
        self.sidebar.title = "Sidebar"
        self.sidebar.set_style("text_below_icon")
        self.sidebar.setFloatable(False)
        self.sidebar.set_allowed_areas("all")
        self.sidebar.set_icon_size(60)
        self.spacer_action = self.sidebar.add_spacer()
        self.add_toolbar(self.sidebar, "left")
        self.area = widgets.Widget()
        self.area.set_layout("stacked")

        main_layout = widgets.BoxLayout("horizontal")
        main_layout.addWidget(self.area)
        w = widgets.Widget()
        w.set_layout(main_layout)
        self.setCentralWidget(w)

    def add_tab(self,
                item,
                title: str,
                icon: icons.IconType = None,
                show: bool = False,
                shortcut: Optional[str] = None,
                area: str = "top"):
        page = item
        self.area.box.add(page)
        # button = widgets.ToolButton()
        # button.set_text(title)
        # button.set_icon_size(40)
        # button.setFixedSize(80, 80)
        # button.set_icon(icon)
        # button.clicked.connect(lambda: self.area.box.setCurrentWidget(page))
        # self.sidebar.addWidget(button)
        # self.sidebar.add_separator()
        if area == "top":
            act = widgets.Action(text=title,
                                 icon=icon,
                                 shortcut=shortcut,
                                 parent=self.sidebar)
            act.setCheckable(True)
            act.triggered.connect(lambda: self.set_tab(page))
            self.sidebar.insertAction(self.spacer_action, act)
        else:
            act = self.sidebar.add_action(title,
                                          icon,
                                          lambda: self.set_tab(page),
                                          checkable=True)
        button = self.sidebar.widgetForAction(act)
        if len(self.area.box) == 1:
            button.setChecked(True)
        page._button = button
        if show:
            self.area.box.setCurrentWidget(page)
        return page

    def set_tab(self, item: Union[int, widgets.Widget]):
        if isinstance(item, int):
            item = self.area.box[item]
        if item not in self.area.box:
            raise ValueError("Layout does not contain the chosen widget")
        current = self.area.box.currentWidget()
        current._button.setChecked(False)
        self.area.box.setCurrentWidget(item)
        item._button.setChecked(True)

    def show_tab(self, index):
        widget = self.area.box[index]
        self.area.box.setCurrentWidget(widget)

    def add_spacer(self):
        self.sidebar.add_spacer()

    def add_separator(self, text: Optional[str] = None, area: str = "top"):
        if area == "top":
            self.sidebar.add_separator(text, before=self.spacer_action)
        else:
            self.sidebar.add_separator(text)

    def add_action(self,
                   title: str,
                   icon: icons.IconType = None,
                   callback: Callable = None,
                   checkable: bool = False,
                   shortcut: Optional[str] = None,
                   area: str = "top"):
        # act = self.sidebar.add_action(label=title,
        #                                      icon=icon,
        #                                      callback=callback,
        #                                      checkable=checkable)
        act = widgets.Action(text=title,
                             icon=icon,
                             shortcut=shortcut)
        act.setCheckable(checkable)
        if callback:
            act.triggered.connect(callback)
        if area == "top":
            self.sidebar.insertAction(self.spacer_action, act)
        if area == "bottom":
            self.sidebar.addAction(act)
        return act


if __name__ == '__main__':
    app = widgets.app()
    ex = SidebarWidget()
    page_1 = widgets.PlainTextEdit()
    page_2 = widgets.ColorDialog()
    page_3 = widgets.FileDialog()
    ex.add_tab(page_1, "Text", "mdi.timer")
    ex.add_tab(page_2, "Color", "mdi.format-color-fill", area="bottom")
    ex.add_tab(page_3, "Help", "mdi.help-circle-outline")
    # ex.show_tab(0)
    ex.show()
    app.exec_()
