from __future__ import annotations

import contextlib

from qstylizer import parser

from prettyqt import gui


class QssValidator(gui.Validator):
    """Validator which checks whether given string is a parseable css string."""

    ID = "qss"

    def __eq__(self, other: object):
        return isinstance(other, QssValidator)

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
        with contextlib.suppress(ValueError):
            if not text or parser.parse(text):
                return self.State.Acceptable, text, pos
        return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = QssValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    with app.debug_mode():
        app.exec()
    print(widget.hasAcceptableInput())
