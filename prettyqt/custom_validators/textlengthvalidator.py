from __future__ import annotations
import sys

from prettyqt import core, gui


class TextLengthValidator(gui.Validator):
    """Validator which checks whether given text has a specific length."""
    ID = "text_length"

    def __init__(
        self,
        minimum: int | None = None,
        maximum: int | None = None,
        parent: core.QObject | None = None,
    ):
        super().__init__(parent)
        self._minimum = 0 if minimum is None else minimum
        self._maximum = sys.maxsize if maximum is None else maximum

    def set_range(self, minimum: int | None, maximum: int | None):
        self._minimum = 0 if minimum is None else minimum
        self._maximum = sys.maxsize if maximum is None else maximum

    def get_range(self) -> tuple[int | None, int | None]:
        return (self._minimum, self._maximum)

    def set_minimum(self, minimum: int | None):
        self._minimum = 0 if minimum is None else minimum

    def get_minimum(self) -> int:
        return self._minimum

    def set_maximum(self, maximum: int | None):
        self._maximum = sys.maxsize if maximum is None else maximum

    def get_maximum(self) -> int:
        return self._maximum

    def validate(self, text: str, pos: int):
        if self._minimum <= len(text) <= self._maximum:
            return self.State.Acceptable, text, len(text)
        if len(text) <= self._maximum:
            return self.State.Intermediate, text, len(text)
        return self.State.Invalid, text, len(text)

    minimum = core.Property(int, get_minimum, set_minimum)
    maximum = core.Property(int, get_maximum, set_maximum)


if __name__ == "__main__":
    from prettyqt import widgets

    val = TextLengthValidator(maximum=10)
    app = widgets.app()
    widget = widgets.LineEdit("343")
    widget.setValidator(val)
    widget.show()
    app.exec()
