from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtCore


class TextLengthValidator(gui.Validator):
    ID = "text_length"

    def __init__(
        self,
        minimum: int | None = None,
        maximum: int | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self.range: tuple[int | None, int | None] = (minimum, maximum)

    def set_range(self, lower: int | None, upper: int | None):
        self.range = (lower, upper)

    def validate(self, text: str, pos: int):
        left = 0 if self.range[0] is None else self.range[0]
        right = float("inf") if self.range[1] is None else self.range[1]

        if left <= len(text) <= right:
            return self.State.Acceptable, text, len(text)
        if len(text) <= right:
            return self.State.Intermediate, text, len(text)
        return self.State.Invalid, text, len(text)


if __name__ == "__main__":
    from prettyqt import widgets

    val = TextLengthValidator(maximum=10)
    app = widgets.app()
    widget = widgets.LineEdit("343")
    widget.setValidator(val)
    widget.show()
    app.exec()
