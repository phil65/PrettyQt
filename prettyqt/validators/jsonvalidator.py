from __future__ import annotations

from prettyqt import gui


class JsonValidator(gui.Validator):
    """Validator which checks for strings which can be parsed as JSON."""

    ID = "json"

    def __eq__(self, other: object):
        return isinstance(other, JsonValidator)

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        import anyenv

        try:
            anyenv.load_json(text)
        except anyenv.JsonLoadError:
            return self.State.Intermediate, text, pos
        else:
            return self.State.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = JsonValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    app.exec()
