from __future__ import annotations

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
        state, text, pos = self._validator.validate(text, pos)
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
