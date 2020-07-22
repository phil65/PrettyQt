# -*- coding: utf-8 -*-
"""
"""

from typing import List, Optional

from qtpy import QtCore
from prettyqt import gui


class CompositeValidator(gui.Validator):
    def __init__(
        self,
        validators: List[gui.Validator] = None,
        parent: Optional[QtCore.QObject] = None,
    ):
        super().__init__(parent)
        self.validators = validators if validators is not None else []

    def __repr__(self):
        return f"CompositeValidator({self.validators})"

    def __getstate__(self):
        return dict(validators=self.validators)

    def __setstate__(self, state):
        self.__init__()
        self.validators = state.get("validators", [])

    def validate(self, text: str, pos: int = 0) -> tuple:
        vals = [v.validate(text, pos)[0] for v in self.validators]
        return (min(vals), text, pos)


if __name__ == "__main__":
    from prettyqt import custom_validators, widgets

    val1 = custom_validators.NotEmptyValidator()
    val2 = custom_validators.PathValidator()
    val = CompositeValidator([val1, val2])
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
