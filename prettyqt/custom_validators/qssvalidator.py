from __future__ import annotations

from qstylizer import parser

from prettyqt import gui
from prettyqt.qt import QtGui


class QssValidator(gui.Validator):
    ID = "qss"

    def __eq__(self, other: object):
        return isinstance(other, QssValidator)

    def validate(
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        try:
            if not text or parser.parse(text):
                return self.State.Acceptable, text, pos
        except ValueError:
            pass
        return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = QssValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    with app.debug_mode():
        app.main_loop()
    print(widget.hasAcceptableInput())
