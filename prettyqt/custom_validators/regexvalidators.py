# -*- coding: utf-8 -*-
"""
"""

from typing import Optional

from qtpy import QtCore
import regex as re

from prettyqt import gui


class BaseRegexValidator(gui.Validator):
    def __init__(
        self, parent: Optional[QtCore.QObject] = None, regex: Optional[str] = None
    ):
        super().__init__(parent)
        self.regex = None
        if regex:
            self.set_regex(regex)

    def __repr__(self):
        return f"BaseRegexValidator({self.get_regex()!r})"

    def __getstate__(self):
        return dict(regexp=self.regex)

    def __setstate__(self, state):
        self.__init__()
        self.set_regex(state["regexp"])

    def set_regex(self, regex: str):
        self.regex = re.compile(regex)

    def get_regex(self) -> str:
        if self.regex is None:
            raise TypeError("Validator not initialized")
        return self.regex.pattern

    def validate(self, text: str, pos: int = 0) -> tuple:
        if self.regex is None:
            raise TypeError("Validator not initialized")
        if text == "":
            return (self.Intermediate, text, pos)
        match = self.regex.match(text, partial=True)
        if match is None:
            return (self.Invalid, text, pos)
        if match.partial:
            return (self.Intermediate, text, pos)
        else:
            return (self.Acceptable, text, pos)


class IntListValidator(BaseRegexValidator):
    def __init__(self, allow_single: bool = True, parent=None):
        super().__init__(parent=parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\d+)(,\s*\d+)*$")
        else:
            self.set_regex(r"^[0-9][0-9\,]+[0-9]$")

    def __repr__(self):
        return f"IntListValidator(allow_single={self.allow_single})"


class FloatListValidator(BaseRegexValidator):
    def __init__(self, allow_single: bool = True, parent=None):
        super().__init__(parent=parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$")
        else:
            self.set_regex(
                r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)" r"(\s*,\s*-?\d+(\.\d+)?)*$"
            )

    def __repr__(self):
        return f"FloatListValidator(allow_single={self.allow_single})"


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.LineEdit()
    val = BaseRegexValidator()
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.exec_()
