from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from typing import Any, Literal

from prettyqt import constants, core, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


TypeStr = Literal["string", "int", "float"]


class SelectionWidget(widgets.GroupBox):
    value_changed = core.Signal(object)

    def __init__(
        self,
        label: str = "",
        layout: constants.OrientationStr = "horizontal",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(title=label, parent=parent)
        self.box = widgets.BoxLayout(layout)
        self.widget_custom: widgets.Widget | None = None
        self.rb_other = widgets.RadioButton()
        self.buttons: dict[widgets.RadioButton, Any] = {}
        self.set_layout(self.box)

    def __iter__(self) -> Iterator[tuple[widgets.RadioButton, Any]]:
        return iter(self.buttons.items())

    def add_items(self, items: Iterable | Mapping):
        if isinstance(items, Mapping):
            for k, v in items.items():
                self.add(v, k)
        else:
            for i in items:
                if isinstance(i, (tuple, list)):
                    self.add(*i)
                else:
                    self.add(i)

    def select_radio_by_data(self, value):
        for rb, data in self.buttons.items():
            if data == value:
                rb.setChecked(True)
                break

    def add(self, title: str, data=None, icon: types.IconType = None):
        # TODO: make use of icon kwarg
        rb = widgets.RadioButton(title)
        rb.toggled.connect(self.update_choice)
        self.buttons[rb] = data
        if len(self.buttons) == 1:
            with rb.block_signals():
                rb.set_value(True)
        self.box.add(rb)

    def add_tooltip_icon(self, text: str):
        label = widgets.Label(text)
        label.setToolTip(text)
        icon = iconprovider.get_icon("mdi.help-circle-outline")
        pixmap = icon.pixmap(20, 20)
        label.setPixmap(pixmap)
        self.box.add(label)

    def add_custom(
        self,
        label: str = "Other",
        typ: TypeStr = "string",
        default: None | float | str = None,
        regex: str | None = None,
    ):
        if typ == "string":
            self.widget_custom = widgets.LineEdit()
        elif typ == "int":
            self.widget_custom = widgets.SpinBox()
        elif typ == "float":
            self.widget_custom = widgets.DoubleSpinBox()
        else:
            raise ValueError(typ)
        # TODO: Enable this or add BAR radio and option.
        self.widget_custom.set_disabled()  # type: ignore
        if default is not None:
            self.widget_custom.set_value(default)  # type: ignore
        self.rb_other.setText(label)
        self.rb_other.toggled.connect(self.widget_custom.set_enabled)  # type: ignore
        self.widget_custom.value_changed.connect(  # type: ignore
            lambda: self.update_choice(True)
        )
        if regex and typ == "string":
            self.widget_custom.set_regex_validator(regex)  # type: ignore
        layout = widgets.BoxLayout("horizontal")
        layout.add(self.rb_other)
        layout.add(self.widget_custom)
        self.box.add(layout)

    def current_choice(self) -> Any:
        for k, v in self.buttons.items():
            if k.isChecked():
                return v
        if self.rb_other.isChecked() and self.widget_custom is not None:
            return self.widget_custom.get_value()
        return None

    @core.Slot(bool)
    def update_choice(self, checked: bool):
        if not checked:
            return
        choice = self.current_choice()
        if choice is not None:
            self.value_changed.emit(choice)

    def set_value(self, value):
        self.select_radio_by_data(value)

    def get_value(self):
        return self.current_choice()


if __name__ == "__main__":
    app = widgets.app()
    widget = SelectionWidget(layout="horizontal")
    items = {";": "Semicolon", "\t": "Tab", ",": "Comma"}
    widget.add_items(items)
    widget.add_custom(label="custom", typ="float")
    widget.show()
    app.main_loop()
    print(widget.get_value())
