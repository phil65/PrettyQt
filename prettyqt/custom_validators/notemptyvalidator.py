from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class NotEmptyValidator(gui.Validator):
    def __eq__(self, other: object):
        return isinstance(other, NotEmptyValidator)

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        if text == "":
            return (self.State.Intermediate, text, pos)
        return self.State.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = NotEmptyValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
