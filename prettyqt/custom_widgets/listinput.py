# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import custom_validators, widgets
from prettyqt.utils import helpers


class ListInput(widgets.LineEdit):

    def __init__(self, default_value="", typ=int, allow_single=False, parent=None):
        super().__init__(parent=parent)
        self.textChanged.connect(self.set_validation_color)
        self.textChanged.connect(self.value_changed)
        if typ is int:
            val = custom_validators.IntListValidator(allow_single=allow_single)
        elif typ is float:
            val = custom_validators.FloatListValidator(allow_single=allow_single)
        else:
            raise ValueError(f"Invalid type {typ}")
        self.set_validator(val)
        self.set_value(default_value)

    def get_value(self) -> list:
        return helpers.string_to_num_array(self.text())

    def set_value(self, value):
        if isinstance(value, list):
            value = str(value)[1:-1].replace(" ", "")
        self.set_text(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = ListInput()
    widget.show()
    app.exec_()
    print(widget.get_value())
