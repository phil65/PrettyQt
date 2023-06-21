from __future__ import annotations

from prettyqt import gui


class AlphaNumericValidator(gui.Validator):
    ID = "alphanumeric"

    def __eq__(self, other: object):
        return isinstance(other, AlphaNumericValidator)

    def validate(self, text: str, pos: int = 0):
        if text.replace("_", "").isalnum():
            return self.State.Acceptable, text, pos
        return self.State.Invalid, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = AlphaNumericValidator()
    app = widgets.app()
    widget = widgets.LineEdit("Thisisatest")
    widget.setValidator(val)
    widget.show()
    app.exec()
