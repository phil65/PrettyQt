from prettyqt import widgets


class SidebarWidget(widgets.MainWindow):

    def __init__(self):
        super().__init__()
        self.sidebar_widget = widgets.ToolBar()
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

    def add_tab(self, title, widget, icon=None, show=True):
        page = widgets.MainWindow()
        page.setCentralWidget(widget)
        self.area.box.add(page)
        # button = widgets.ToolButton()
        # button.set_text(title)
        # button.set_icon_size(40)
        # button.setFixedSize(80, 80)
        # button.set_icon(icon)
        # button.clicked.connect(lambda: self.area.box.setCurrentWidget(page))
        # self.sidebar_widget.addWidget(button)
        self.sidebar_widget.add_separator()
        act = self.sidebar_widget.add_action(title,
                                             icon,
                                             lambda: self.set_tab(page),
                                             checkable=True)
        button = self.sidebar_widget.widgetForAction(act)
        if len(self.area.box) == 1:
            button.setChecked(True)
        page._button = button
        self.area.box.setCurrentWidget(page)

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
    ex.add_tab("Text", page_1, "mdi.timer")
    ex.add_tab("Color", page_2, "mdi.format-color-fill")
    ex.add_tab("Help", page_3, "mdi.help-circle-outline")
    ex.show_tab(0)
    ex.show()
    app.exec_()
