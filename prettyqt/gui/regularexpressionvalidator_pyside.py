# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, gui


class RegularExpressionValidator(gui.Validator):

    def __init__(self, regex=None):
        super().__init__()
        self.regex = None
        self.set_regex(regex)

    def __repr__(self):
        return f"RegularExpressionValidator(RegularExpression({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(regexp=core.RegularExpression(self.regularExpression()))

    def __setstate__(self, state):
        self.__init__()
        self.regex = state["regexp"]

    def setRegularExpression(self, re):
        self.regex = re

    def regularExpression(self):
        return self.regex

    def set_regex(self, regex: str, flags=0):
        self.regex = core.RegularExpression(regex, flags)

    def get_regex(self) -> str:
        return self.regex.pattern()

    def validate(self, text, pos=0):
        if text == "":
            return (self.Intermediate, text, pos)
        match = self.regex.match(text, match_type="prefer_first")
        if match.hasPartialMatch():
            return (self.Intermediate, text, pos)
        if match.hasMatch():
            return (self.Acceptable, text, pos)
        return (self.Invalid, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    w = widgets.LineEdit()
    val = RegularExpressionValidator()
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.exec_()
