from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from prettyqt import constants, gui, iconprovider, widgets


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


AreaStr = Literal["top", "bottom"]


class SidebarWidget(widgets.MainWindow):
    SETTINGS_BUTTON_HEIGHT = 28

    def __init__(
        self,
        *args,
        show_settings: bool = False,
        main_layout: widgets.widget.LayoutStr | widgets.QLayout = "vertical",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._button_width = 100
        self._style: constants.ToolButtonStyleStr = "text_below_icon"
        self.button_map: dict[widgets.QWidget, widgets.QToolButton] = {}
        self.icon_map: dict[widgets.QWidget, gui.Icon] = {}
        self.sidebar = widgets.ToolBar(
            context_menu_policy="prevent",
            floatable=True,
            object_name="SidebarWidget",
            window_title="Sidebar",
        )
        self.sidebar.set_style(self._style)
        self.sidebar.set_allowed_areas("all")
        self.settings_menu = widgets.Menu()
        self.sidebar.set_icon_size(int(self._button_width * 0.7))
        if show_settings:
            self.settings_btn = self.sidebar.add_menu_button(
                "", icon="mdi.wrench", menu=self.settings_menu
            )
            self.settings_btn.setFixedSize(
                self._button_width, self.SETTINGS_BUTTON_HEIGHT
            )
            self.settings_btn.set_style("icon")
            self.sidebar.orientationChanged.connect(self._on_orientation_change)
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

    def _on_orientation_change(self, orientation: constants.Orientation):
        if orientation == constants.HORIZONTAL:
            self.settings_btn.setFixedSize(34, 34)
        else:
            self.settings_btn.setFixedSize(
                self._button_width, self.SETTINGS_BUTTON_HEIGHT
            )

    def add_tab(
        self,
        item: widgets.QWidget,
        title: str,
        icon: datatypes.IconType | None = None,
        show: bool = False,
        shortcut: str | None = None,
        area: AreaStr = "top",
    ):
        self.area.box.add(item)
        act = gui.Action(
            text=title,
            icon=icon,
            shortcut=shortcut or "",
            parent=self.sidebar,
            checkable=True,
            triggered=lambda: self.set_tab(item),
        )
        self.addAction(act)
        button = widgets.ToolButton(self.sidebar)
        button.setDefaultAction(act)
        button.setFixedWidth(self._button_width)
        button.set_style(self._style)
        if area == "top":
            self.sidebar.insertWidget(self.spacer_action, button)
        else:
            self.sidebar.addWidget(button)
        if len(self.area.box) == 1:
            button.setChecked(True)
        self.button_map[item] = button
        self.icon_map[item] = iconprovider.get_icon(icon)
        if show:
            self.area.box.setCurrentWidget(item)

    def set_marker(
        self, item: str | int | widgets.Widget, color: datatypes.ColorType = "red"
    ):
        widget = item if isinstance(item, widgets.QWidget) else self._get_widget(item)
        if widget == self._get_current_widget():
            return
        template = self.icon_map[widget]
        px = template.pixmap(100, 100)
        with gui.Painter(px) as painter:
            dot = gui.Pixmap.create_dot(color)
            painter.drawPixmap(0, 0, dot)
        icon = gui.Icon(px)
        self.button_map[widget].setIcon(icon)

    def _get_widget(self, item: str | int | widgets.Widget):
        """Returns widget page specified by name, offset or content."""
        match item:
            case int():
                return self.area.box[item]
            case str():
                w = self.area.find_child(widgets.QWidget, name=item, recursive=False)
                if w not in self.area.box:
                    msg = "Layout does not contain the chosen widget"
                    raise ValueError(msg)
                return w
            case _:
                raise TypeError(item)

    def _get_current_widget(self) -> widgets.QWidget:
        """Returns the currently selected widget page."""
        for k, v in self.button_map.items():
            if v.isChecked():
                return k
        msg = "no page activated."
        raise RuntimeError(msg)

    def set_tab(self, item: str | int | widgets.QWidget):
        widget = item if isinstance(item, widgets.QWidget) else self._get_widget(item)
        current = self.area.box.currentWidget()
        self.button_map[current].setChecked(False)
        self.area.box.setCurrentWidget(widget)
        self.button_map[widget].setChecked(True)

    def add_spacer(self) -> gui.QAction:
        return self.sidebar.add_spacer()

    def add_separator(self, text: str | None = None, area: AreaStr = "top"):
        if area == "top":
            self.sidebar.add_separator(text, before=self.spacer_action)
        else:
            self.sidebar.add_separator(text)

    def add_action(self, *args, area: AreaStr = "top", **kwargs):
        act = args[0] if args else gui.Action(**kwargs)
        self.addAction(act)
        button = widgets.ToolButton(self.sidebar)
        button.setDefaultAction(act)
        button.setFixedWidth(self._button_width)
        button.set_style(self._style)
        if area == "top":
            self.sidebar.insertWidget(self.spacer_action, button)
        else:
            self.sidebar.addWidget(button)
        return act


if __name__ == "__main__":
    from prettyqt.custom_widgets import commandpalette

    app = widgets.app()
    a = commandpalette.CommandPalette()
    ex = SidebarWidget(show_settings=True)
    ex.add_shortcut("Ctrl+P", a.show)
    page_1 = widgets.PlainTextEdit()
    page_2 = widgets.ColorDialog()
    page_3 = widgets.FileDialog()
    ex.add_tab(page_1, "Text", "mdi.timer")
    ex.add_tab(page_2, "Color", "mdi.format-color-fill", area="bottom")
    ex.add_tab(page_3, "Help", "mdi.help-circle-outline")
    ex.set_marker(page_3)
    a.populate_from_widget(ex)
    ex.show()
    app.exec()
