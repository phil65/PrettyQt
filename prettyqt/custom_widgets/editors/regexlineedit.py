from __future__ import annotations

from re import Pattern

from prettyqt import custom_widgets, validators, widgets


class RegexLineEdit(custom_widgets.SingleLineTextEdit):
    def __init__(self, *args, object_name: str = "regex_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_syntaxhighlighter("regex")
        self.val = validators.RegexPatternValidator()
        self.set_margin(0)
        self.set_validator(self.val)

    @property
    def pattern(self) -> str:
        return self.text()

    @pattern.setter
    def pattern(self, value: str):
        self.set_text(value)

    def set_value(self, value: str | Pattern | None):
        match value:
            case None:
                self.pattern = ""
            case str():
                self.pattern = value
            case _:
                self.pattern = value.pattern


if __name__ == "__main__":
    app = widgets.app()
    widget = RegexLineEdit()
    widget.show()
    widget.value_changed.connect(print)
    app.exec()
