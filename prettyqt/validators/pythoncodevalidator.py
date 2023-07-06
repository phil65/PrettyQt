from __future__ import annotations

import ast

from prettyqt import gui


class PythonCodeValidator(gui.Validator):
    """Validator which checks whether given string is valid Python code."""

    ID = "python_code"

    def __eq__(self, other: object):
        return isinstance(other, PythonCodeValidator)

    def validate(self, text: str, pos: int = 0) -> tuple[gui.QValidator.State, str, int]:
        try:
            ast.parse(text)
            return self.State.Acceptable, text, pos
        except SyntaxError:
            return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = PythonCodeValidator()
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.setValidator(val)
    widget.show()
    app.exec()
