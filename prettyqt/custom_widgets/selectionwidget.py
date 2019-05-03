# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, widgets


class SelectionWidget(widgets.GroupBox):
    option_changed = core.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = widgets.BoxLayout("horizontal")
        self.rb_other = widgets.RadioButton("Other")
        self.buttons = dict()
        # self.rb_comma.setChecked(True)

        self.setLayout(self.layout)

    def __iter__(self):
        return iter(self.buttons.items())

    def add_items(self, dct):
        for k, v in dct.items():
            self.add_item(k, v)

    def select_radio_by_data(self, value):
        for rb, data in self.buttons.items():
            if data == value:
                rb.setChecked(True)

    def add_item(self, title, data=None):
        rb = widgets.RadioButton(title)
        rb.toggled.connect(self.update_choice)
        self.buttons[rb] = data
        if len(self.buttons) == 1:
            rb.setChecked(True)
        self.layout.addWidget(rb)

    def add_custom(self, regex):
        self.lineedit_custom_sep = widgets.LineEdit(self)
        # TODO: Enable this or add BAR radio and option.
        self.lineedit_custom_sep.setEnabled(False)
        self.rb_other.toggled.connect(self.lineedit_custom_sep.setEnabled)
        self.lineedit_custom_sep.textChanged.connect(lambda: self.update_choice(True))
        self.lineedit_custom_sep.set_regex_validator(regex)
        self.layout.addWidget(self.rb_other)
        self.layout.addWidget(self.lineedit_custom_sep)

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
        if len(choice) > 0:
            self.option_changed.emit(choice)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = SelectionWidget()
    items = {"Semicolon": ";",
             "Tab": "\t",
             "Comma": ","}
    widget.add_items(items)
    widget.add_custom(regex=r"\S{1}")
    widget.show()
    app.exec_()
