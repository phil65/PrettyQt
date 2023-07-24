from __future__ import annotations

import sys

from prettyqt import core, gui


class IntegerValidator(gui.Validator):
    """Validator to check for integer values.

    In contrast to IntValidator provided by Qt, this validator is not bound to
    a restricted value range.
    """

    ID = "integer"

    def __init__(
        self,
        bottom: int | None = None,
        top: int | None = None,
        parent: core.QObject | None = None,
    ):
        super().__init__(parent)
        self._bottom = -sys.maxsize if bottom is None else bottom
        self._top = sys.maxsize if top is None else top

    def set_range(self, lower: int | None, upper: int | None):
        self.set_top(upper)
        self.set_bottom(lower)

    def get_range(self) -> tuple[int, int]:
        return (self._bottom, self._top)

    def set_bottom(self, bottom: int | None):
        self._bottom = -sys.maxsize if bottom is None else bottom

    def get_bottom(self) -> int:
        return self._bottom

    def set_top(self, top: int | None):
        self._top = sys.maxsize if top is None else top

    def get_top(self) -> int:
        return self._top

    def validate(self, text: str, pos: int):
        if not text.lstrip("-"):
            return self.State.Intermediate, text, len(text)
        if text.lstrip("-").isnumeric():
            left = float("-inf") if self._bottom is None else self._bottom
            right = float("inf") if self._top is None else self._top
            if left <= int(text) <= right:
                return self.State.Acceptable, text, len(text)
        return self.State.Invalid, text, len(text)

    bottom = core.Property(
        int,
        get_bottom,
        set_bottom,
        doc="Minimum value",
    )
    top = core.Property(
        int,
        get_top,
        set_top,
        doc="Maximum value",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    val = IntegerValidator()
    app = widgets.app()
    widget = widgets.LineEdit("343")
    widget.setValidator(val)
    widget.show()
    app.exec()
