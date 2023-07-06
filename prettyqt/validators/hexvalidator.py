from __future__ import annotations

from prettyqt import gui


class HexValidator(gui.Validator):
    """Validator which checks for hexadecimal values."""

    ID = "hex"

    def __init__(self, maximum: int | None = None, parent=None):
        super().__init__(parent)
        self._maximum = maximum

    def __eq__(self, other: object):
        return isinstance(other, HexValidator) and other._maximum == self._maximum

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
        try:
            val = int(text, 0)
        except ValueError:
            return self.State.Intermediate, text, pos
        if self._maximum is not None and val > self._maximum:
            return self.State.Invalid, text, pos
        return self.State.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = HexValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    with app.debug_mode():
        app.exec()
    print(widget.hasAcceptableInput())
