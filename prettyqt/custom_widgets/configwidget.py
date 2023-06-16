from __future__ import annotations

from typing import Any

from dataclasses import dataclass
from prettyqt import custom_widgets, widgets


@dataclass
class BaseSetting:
    identifier: str
    label: str
    description: str
    requires_restart: bool = False


@dataclass
class SelectionSetting(BaseSetting):
    options: list[str] | None = None
    default: Any = None
    minimum: float = 0.0
    maximum: float = 0.0
    pattern: str = ""
    requires_restart: bool = False


@dataclass
class BoolSetting(BaseSetting):
    default: bool = False


@dataclass
class IntSetting(BaseSetting):
    options: list[str] | None = None
    default: Any = None
    minimum: int | None = None
    maximum: int | None = None


@dataclass
class StrSetting(BaseSetting):
    default: Any = None
    minimum: int | None = None
    maximum: int | None = None


class SettingsWindow(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = self.set_layout("horizontal")
        self.configwidget = widgets.Widget()
        self.configwidget.set_max_width(600)
        self.configwidget.set_layout("vertical")
        self.scrollarea = widgets.ScrollArea()
        self.scrollarea.set_widget(self.configwidget)
        self.toc = custom_widgets.ScrollAreaTocWidget(self.scrollarea)
        layout.add(self.toc)
        layout.add(self.scrollarea)

    def add_setting(self, setting: BaseSetting):
        row_widget = widgets.GroupBox(window_title=setting.label)
        layout = row_widget.set_layout("vertical")
        header_label = widgets.Label(setting.label)
        with header_label.edit_font() as font:
            font.setPointSize(14)
        layout.add(header_label)
        if setting.requires_restart:
            label = widgets.Label("(requires restart)")
            label.set_color("red")
            layout.add(label)
        match setting:
            case SelectionSetting():
                widget = widgets.ComboBox()
                widget.add_items(setting.options)
            case BoolSetting():
                widget = widgets.CheckBox()
            case StrSetting():
                widget = widgets.LineEdit()
            case IntSetting():
                widget = widgets.SpinBox()
                widget.set_range(setting.minimum, setting.maximum)

        container = widgets.Widget()
        row_layout = container.set_layout("horizontal")
        row_layout.add(widget)
        row_layout.add(widgets.Label(setting.description), stretch=1)
        if setting.default is not None:
            widget.set_value(setting.default)
        layout.add(container)
        self.configwidget.box.add(row_widget)
        self.scrollarea.ensureWidgetVisible(row_widget)
        self.scrollarea.setWidgetResizable(True)


if __name__ == "__main__":
    app_style = SelectionSetting(
        identifier="app_style",
        label="App style",
        description="Set the app style",
        options=widgets.StyleFactory.keys(),
        requires_restart=True,
        default=None,
    )

    bool_test = BoolSetting(
        identifier="bool_setting",
        label="Bool setting",
        description="This setting is a bool.",
        default=True,
    )
    int_test = IntSetting(
        identifier="int_setting",
        label="Int setting",
        description="This setting is an int.",
        default=15,
        minimum=10,
        maximum=20,
    )

    str_test = StrSetting(
        identifier="str_setting",
        label="Str setting",
        description="Some longer text",
        requires_restart=True,
        default="hallo",
    )

    app = widgets.app()
    widget = SettingsWindow()
    widget.add_setting(app_style)
    widget.add_setting(bool_test)
    widget.add_setting(bool_test)
    widget.add_setting(bool_test)
    widget.add_setting(str_test)
    widget.add_setting(int_test)
    widget.add_setting(str_test)
    widget.add_setting(str_test)
    widget.add_setting(app_style)
    widget.add_setting(app_style)
    widget.add_setting(app_style)
    widget.add_setting(app_style)
    widget.show()
    app.main_loop()
