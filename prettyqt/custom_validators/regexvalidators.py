from __future__ import annotations

import re

from prettyqt import gui
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class BaseRegexValidator(gui.Validator):
    ID = "regex"

    def __init__(
        self,
        parent: QtCore.QObject | None = None,
        regex: datatypes.PatternType | None = None,
    ):
        super().__init__(parent)
        self.regex: re.Pattern | None = None
        if regex:
            self.set_regex(regex)

    def __repr__(self):
        return get_repr(self, self.get_regex())

    def __reduce__(self):
        return type(self), (self.get_regex(),)

    def __eq__(self, other: object):
        return self.regex == other.regex if isinstance(other, type(self)) else False

    def set_regex(self, regex: datatypes.PatternAndStringType):
        self.regex = datatypes.to_py_pattern(regex)

    def get_regex(self) -> str:
        if self.regex is None:
            raise TypeError("Validator not initialized")
        return self.regex.pattern

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        if self.regex is None:
            raise TypeError("Validator not initialized")
        if not text:
            return self.State.Intermediate, text, pos
        match = self.regex.match(text)  # type: ignore
        if match is None:
            #     return self.State.Invalid, text, pos
            # elif match.partial:  # type: ignore
            return self.State.Intermediate, text, pos
        else:
            return self.State.Acceptable, text, pos


class IntListValidator(BaseRegexValidator):
    ID = "int_list"

    def __init__(self, allow_single: bool = True, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\d+)(,\s*\d+)*$")
        else:
            self.set_regex(r"^[0-9][0-9\,]+[0-9]$")

    def __reduce__(self):
        return type(self), (self.allow_single,)

    def __repr__(self):
        return get_repr(self, allow_single=self.allow_single)


class FloatListValidator(BaseRegexValidator):
    ID = "float_list"

    def __init__(self, allow_single: bool = True, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$")
        else:
            self.set_regex(
                r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$"
            )

    def __reduce__(self):
        return type(self), (self.allow_single,)

    def __repr__(self):
        return get_repr(self, allow_single=self.allow_single)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.LineEdit()
    val = BaseRegexValidator()
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.exec()
