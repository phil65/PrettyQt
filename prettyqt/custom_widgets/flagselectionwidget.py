# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, widgets


class FlagSelectionWidget(widgets.GroupBox):
    value_changed = core.Signal(int)

    def __init__(self, label="", layout="vertical", parent=None):
        super().__init__(title=label, parent=parent)
        self.box = widgets.BoxLayout(layout)
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

    def add(self, title: str, flag):
        checkbox = widgets.CheckBox(title)
        checkbox.toggled.connect(self.update_choice)
        self.buttons[checkbox] = flag
        self.box += checkbox

    def current_choice(self):
        ret_val = 0
        for btn, flag in self.buttons.items():
            if btn.isChecked():
                ret_val |= flag
        return int(ret_val)

    @core.Slot(bool)
    def update_choice(self, checked):
        choice = self.current_choice()
        self.value_changed.emit(choice)

    def set_value(self, value):
        value = int(value)
        for btn, flag in self.buttons.items():
            btn.setChecked(bool(value & flag))

    def get_value(self):
        return self.current_choice()


if __name__ == "__main__":
    import re
    app = widgets.app()
    widget = FlagSelectionWidget()
    items = {"MultiLine": re.MULTILINE,
             "Ignore case": re.IGNORECASE}
    widget.add_items(items)
    widget.show()
    app.exec_()
    print(widget.get_value())
