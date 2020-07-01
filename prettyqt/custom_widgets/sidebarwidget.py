# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import widgets


class SidebarWidget(widgets.MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.sidebar_widget = widgets.ToolBar()
        self.sidebar_widget.id = "SidebarWidget"
        self.sidebar_widget.title = "Sidebar"
        self.sidebar_widget.set_style("text_below_icon")
        self.sidebar_widget.setFloatable(False)
        self.sidebar_widget.set_allowed_areas("all")
        self.sidebar_widget.set_icon_size(60)
        self.add_toolbar(self.sidebar_widget, "left")
        self.area = widgets.Widget()
        self.area.set_layout("stacked")

        main_layout = widgets.BoxLayout("horizontal")
        main_layout.addWidget(self.area)
        w = widgets.Widget()
        w.set_layout(main_layout)
        self.setCentralWidget(w)

    def add_tab(self, item, title: str, icon=None, show: bool = False):
        page = item
        self.area.box.add(page)
        # button = widgets.ToolButton()
        # button.set_text(title)
        # button.set_icon_size(40)
        # button.setFixedSize(80, 80)
        # button.set_icon(icon)
        # button.clicked.connect(lambda: self.area.box.setCurrentWidget(page))
        # self.sidebar_widget.addWidget(button)
        # self.sidebar_widget.add_separator()
        act = self.sidebar_widget.add_action(title,
                                             icon,
                                             lambda: self.set_tab(page),
                                             checkable=True)
        button = self.sidebar_widget.widgetForAction(act)
        if len(self.area.box) == 1:
            button.setChecked(True)
        page._button = button
        if show:
            self.area.box.setCurrentWidget(page)
        return page

    def set_tab(self, widget):
        current = self.area.box.currentWidget()
        current._button.setChecked(False)
        self.area.box.setCurrentWidget(widget)
        widget._button.setChecked(True)

    def show_tab(self, index):
        widget = self.area.box[index]
        self.area.box.setCurrentWidget(widget)


if __name__ == '__main__':
    app = widgets.app()
    ex = SidebarWidget()
    page_1 = widgets.PlainTextEdit()
    page_2 = widgets.ColorDialog()
    page_3 = widgets.FileDialog()
    ex.add_tab(page_1, "Text", "mdi.timer")
    ex.add_tab(page_2, "Color", "mdi.format-color-fill")
    ex.add_tab(page_3, "Help", "mdi.help-circle-outline")
    # ex.show_tab(0)
    ex.show()
    app.exec_()
