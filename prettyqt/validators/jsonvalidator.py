from __future__ import annotations

import json

from prettyqt import gui


class JsonValidator(gui.Validator):
    """Validator which checks for strings which can be parsed as JSON."""

    ID = "json"

    def __eq__(self, other: object):
        return isinstance(other, JsonValidator)

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        try:
            json.loads(text)
            return self.State.Acceptable, text, pos
        except json.decoder.JSONDecodeError:
            return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = JsonValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    app.exec()
