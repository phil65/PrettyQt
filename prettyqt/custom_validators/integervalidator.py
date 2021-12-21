from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtCore


class IntegerValidator(gui.Validator):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.range: tuple[int | None, int | None] = (None, None)

    def set_range(self, lower: int | None, upper: int | None):
        self.range = (lower, upper)

    def validate(self, text: str, pos: int):
        if not text.lstrip("-"):
            return self.State.Intermediate, text, len(text)
        if text.lstrip("-").isnumeric():
            left = float("-inf") if self.range[0] is None else self.range[0]
            right = float("inf") if self.range[1] is None else self.range[1]
            if left <= int(text) <= right:
                return self.State.Acceptable, text, len(text)
        return self.State.Invalid, text, len(text)


if __name__ == "__main__":
    from prettyqt import widgets

    val = IntegerValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
