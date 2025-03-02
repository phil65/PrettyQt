from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import gui


if TYPE_CHECKING:
    from prettyqt.qt import QtCore


class WhitelistValidator(gui.Validator):
    """Validator which allows a fixed list of strings."""

    ID = "whitelist"

    def __init__(
        self,
        options: list[str] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self._options = options

    def __eq__(self, other: object):
        return isinstance(other, WhitelistValidator) and self._options == other._options

    def validate(self, text: str, pos: int = 0):
        if any(option == text for option in self._options):
            return self.State.Acceptable, text, pos
        if any(option.startswith(text) for option in self._options):
            return self.State.Intermediate, text, pos
        return self.State.Invalid, text, pos


class EmptyValidator(WhitelistValidator):
    ID = "empty"

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._options = [""]


if __name__ == "__main__":
    from prettyqt import widgets

    val = WhitelistValidator(["a", "abc", "xyz"])
    app = widgets.app()
    widget = widgets.LineEdit("Thisisatest")
    widget.setValidator(val)
    widget.show()
    app.exec()
