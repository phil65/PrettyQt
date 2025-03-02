from __future__ import annotations

from prettyqt import gui


class ColorValidator(gui.Validator):
    """Validator which checks for strings representing a color."""

    ID = "color"

    def __eq__(self, other: object):
        return isinstance(other, ColorValidator)

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
        color = gui.Color(text)
        if color.isValid():
            return self.State.Acceptable, text, pos
        return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = ColorValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    app.exec()
