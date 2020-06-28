# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import regex as re

from prettyqt import gui


class BaseRegexValidator(gui.Validator):

    def __init__(self, regex=None):
        super().__init__()
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
        return self.regex.pattern

    def validate(self, text, pos=0):
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

    def __repr__(self):
        return f"IntListValidator(allow_single={self.allow_single})"

    def __init__(self, allow_single=True, parent=None):
        super().__init__(parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\d+)(,\s*\d+)*$")
        else:
            self.set_regex(r"^[0-9][0-9\,]+[0-9]$")


class FloatListValidator(BaseRegexValidator):

    def __repr__(self):
        return f"FloatListValidator(allow_single={self.allow_single})"

    def __init__(self, allow_single=True, parent=None):
        super().__init__(parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$")
        else:
            self.set_regex(r"^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)"
                           r"(\s*,\s*-?\d+(\.\d+)?)*$")


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    w = widgets.LineEdit()
    val = BaseRegexValidator()
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.exec_()
