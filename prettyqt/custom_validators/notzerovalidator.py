from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class NotZeroValidator(gui.Validator):
    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        if text == "0":
            return self.State.Intermediate, text, pos
        return self.State.Acceptable, text, pos

    def __eq__(self, other: object):
        return isinstance(other, NotZeroValidator)


if __name__ == "__main__":
    from prettyqt import widgets

    val = NotZeroValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
