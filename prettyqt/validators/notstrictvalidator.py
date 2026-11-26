from typing import cast

from prettyqt import gui


class NotStrictValidator(gui.Validator):
    """Validator which turns Invalid state into Intermediate state."""

    ID = "not_strict"

    def __init__(self, validator: gui.QValidator | None = None, **kwargs):
        self._validator = validator
        super().__init__(**kwargs)

    def __eq__(self, other: object):
        return (
            isinstance(other, NotStrictValidator) and other._validator == self._validator
        )

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
        if self._validator is None:
            return self.State.Acceptable, text, pos
        # The PySide6 stubs type validate()'s result as `object`.
        result = cast(
            "tuple[gui.QValidator.State, str, int]", self._validator.validate(text, pos)
        )
        state, text, pos = result
        is_invalid = state == self.State.Invalid
        return self.State.Intermediate if is_invalid else state, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.LineEdit()
    widget.set_validator("alphanumeric", strict=False)
    widget.show()
    with app.debug_mode():
        app.exec()
    print(widget.hasAcceptableInput())
