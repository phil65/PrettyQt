from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import gui


if TYPE_CHECKING:
    from collections.abc import Callable


class FunctionValidator(gui.Validator):
    """Validator which checks based on a given Callable.

    Allows for quickly creating a validator without subclassing.
    """

    ID = "function"

    def __init__(self, fn: Callable[[str], bool], parent=None):
        super().__init__(parent)
        self._fn = fn

    def __eq__(self, other: object):
        return isinstance(other, FunctionValidator) and other._fn == self._fn

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
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
