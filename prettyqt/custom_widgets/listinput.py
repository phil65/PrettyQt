# -*- coding: utf-8 -*-
"""
"""

from typing import List, Union, Optional, Type
from qtpy import QtWidgets
from prettyqt import custom_validators, widgets
from prettyqt.utils import helpers


class ListInput(widgets.LineEdit):
    def __init__(
        self,
        default_value: Union[List[float], str] = "",
        typ: Type = int,
        allow_single: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        if typ is int:
            val = custom_validators.IntListValidator(allow_single=allow_single)
        elif typ is float:
            val = custom_validators.FloatListValidator(allow_single=allow_single)
        else:
            raise ValueError(f"Invalid type {typ}")
        self.set_validator(val)
        self.set_value(default_value)

    def get_value(self) -> List[float]:  # type: ignore[override]
        return helpers.string_to_num_array(self.text())

    def set_value(self, value: Union[List[float], str]):
        if isinstance(value, list):
            value = str(value)[1:-1].replace(" ", "")
        self.set_text(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = ListInput()
    widget.show()
    app.exec_()
    print(widget.get_value())
