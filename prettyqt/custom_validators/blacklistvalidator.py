from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtCore


class BlacklistValidator(gui.Validator):
    ID = "blacklist"

    def __init__(
        self,
        options: list[str] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self._options = options

    def __eq__(self, other: object):
        return isinstance(other, BlacklistValidator) and self._options == other._options

    def validate(self, text: str, pos: int = 0):
        if any(option == text for option in self._options):
            return self.State.Invalid, text, pos
        return self.State.Acceptable, text, pos


class NotZeroValidator(BlacklistValidator):
    ID = "not_zero"

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._options = ["0"]


class NotEmptyValidator(BlacklistValidator):
    ID = "not_empty"

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._options = [""]


if __name__ == "__main__":
    from prettyqt import widgets

    val = BlacklistValidator(["a", "abc", "xyz"])
    app = widgets.app()
    widget = widgets.LineEdit("Thisisatest")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
