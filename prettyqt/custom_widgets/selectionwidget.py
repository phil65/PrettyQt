# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Optional

from prettyqt import core, gui, widgets


class SelectionWidget(widgets.GroupBox):
    value_changed = core.Signal(object)

    def __init__(self, label="", layout="horizontal", parent=None):
        super().__init__(title=label, parent=parent)
        self.box = widgets.BoxLayout(layout)
        self.rb_other = widgets.RadioButton()
        self.buttons = dict()
        self.set_layout(self.box)

    def __iter__(self):
        return iter(self.buttons.items())

    def add_items(self, items):
        if isinstance(items, dict):
            for k, v in items.items():
                self.add(k, v)
        else:
            for i in items:
                if isinstance(i, tuple):
                    self.add(*i)
                else:
                    self.add(i)

    def select_radio_by_data(self, value):
        for rb, data in self.buttons.items():
            if data == value:
                rb.setChecked(True)

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

    def add_custom(self, label: str = "Other", regex: Optional[str] = None):
        self.lineedit_custom_sep = widgets.LineEdit()
        # TODO: Enable this or add BAR radio and option.
        self.lineedit_custom_sep.set_disabled()
        self.rb_other.setText(label)
        self.rb_other.toggled.connect(self.lineedit_custom_sep.set_enabled)
        self.lineedit_custom_sep.textChanged.connect(lambda: self.update_choice(True))
        if regex:
            self.lineedit_custom_sep.set_regex_validator(regex)
        self.box += self.rb_other
        self.box += self.lineedit_custom_sep

    def current_choice(self):
        for k, v in self.buttons.items():
            if k.isChecked():
                return v
        if self.rb_other.isChecked():
            return self.lineedit_custom_sep.text()
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
    items = {"Semicolon": ";",
             "Tab": "\t",
             "Comma": ","}
    widget.add_items(items)
    widget.add_custom(label="custom", regex=r"\S{1}")
    widget.show()
    app.exec_()
