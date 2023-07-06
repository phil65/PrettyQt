from __future__ import annotations

from prettyqt import custom_widgets, validators, widgets
from prettyqt.utils import datatypes


class RegexLineEdit(custom_widgets.SingleLineTextEdit):
    def __init__(self, *args, object_name: str = "regex_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_syntaxhighlighter("regex")
        self.set_margin(0)
        val = validators.RegexPatternValidator()
        self.set_validator(val)

    def set_value(self, value: datatypes.PatternAndStringType | None):
        match value:
            case None:
                self.set_text("")
            case _:
                self.set_text(datatypes.to_py_pattern(value).pattern)


if __name__ == "__main__":
    app = widgets.app()
    widget = RegexLineEdit()
    widget.show()
    widget.value_changed.connect(print)
    app.exec()
