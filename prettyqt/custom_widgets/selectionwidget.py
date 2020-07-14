# -*- coding: utf-8 -*-
"""
"""

from typing import Optional, Mapping, Iterable, Union

from prettyqt import core, gui, widgets


class SelectionWidget(widgets.GroupBox):
    value_changed = core.Signal(object)

    def __init__(self, label="", layout="horizontal", parent=None):
        super().__init__(title=label, parent=parent)
        self.box = widgets.BoxLayout(layout)
        self.widget_custom = None
        self.rb_other = widgets.RadioButton()
        self.buttons = dict()
        self.set_layout(self.box)

    def __iter__(self):
        return iter(self.buttons.items())

    def add_items(self, items: Union[Iterable, Mapping]):
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

    def add(self, title: str, data=None):
        rb = widgets.RadioButton(title)
        rb.toggled.connect(self.update_choice)
        self.buttons[rb] = data
        if len(self.buttons) == 1:
            with rb.block_signals():
                rb.set_value(True)
        self.box += rb

    def add_tooltip_icon(self, text: str):
        label = widgets.Label(text)
        label.setToolTip(text)
        icon = gui.Icon.by_name("mdi.help-circle-outline")
        pixmap = icon.pixmap(core.Size(20, 20))
        label.setPixmap(pixmap)
        self.box += label

    def add_custom(
        self, label: str = "Other", typ: str = "string", regex: Optional[str] = None
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
        self.widget_custom.set_disabled()
        self.rb_other.setText(label)
        self.rb_other.toggled.connect(self.widget_custom.set_enabled)
        self.widget_custom.value_changed.connect(lambda: self.update_choice(True))
        if regex and typ == "string":
            self.widget_custom.set_regex_validator(regex)
        self.box += self.rb_other
        self.box += self.widget_custom

    def current_choice(self):
        for k, v in self.buttons.items():
            if k.isChecked():
                return v
        if self.rb_other.isChecked():
            return self.widget_custom.get_value()
        return

    @core.Slot(bool)
    def update_choice(self, checked):
        if not checked:
            return None
        choice = self.current_choice()
        if choice is not None:
            self.value_changed.emit(choice)

    def set_value(self, value):
        self.select_radio_by_data(value)

    def get_value(self):
        return self.current_choice()


if __name__ == "__main__":
    app = widgets.app()
    widget = SelectionWidget()
    items = {";": "Semicolon", "\t": "Tab", ",": "Comma"}
    widget.add_items(items)
    widget.add_custom(label="custom", typ="float")
    widget.show()
    app.exec_()
    print(widget.get_value())
