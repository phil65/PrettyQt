from __future__ import annotations

from collections.abc import Callable

from prettyqt import gui
from prettyqt.qt import QtGui


class FunctionValidator(gui.Validator):
    ID = "function"

    def __init__(self, fn: Callable[[str], bool], parent=None):
        super().__init__(parent)
        self._fn = fn

    def __eq__(self, other: object):
        return isinstance(other, FunctionValidator) and other._fn == self._fn

    def validate(
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        if self._fn(text):
            return self.State.Acceptable, text, pos
        return self.State.Invalid, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = FunctionValidator(lambda text: text in ["a", "b"])
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.set_validator(val, strict=False)
    widget.show()
    print(widget.validator())
    with app.debug_mode():
        app.exec()
    print(widget.hasAcceptableInput())