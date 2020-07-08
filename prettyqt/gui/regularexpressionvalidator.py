# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtGui

from prettyqt import core, gui


QtGui.QRegularExpressionValidator.__bases__ = (gui.Validator,)


class RegularExpressionValidator(QtGui.QRegularExpressionValidator):
    def __repr__(self):
        return f"RegularExpressionValidator(RegularExpression({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(pattern=core.RegularExpression(self.regularExpression()))

    def __setstate__(self, state):
        self.__init__()
        self.setRegularExpression(state["pattern"])

    def set_regex(self, regex: str, flags=0):
        re = core.RegularExpression(regex, flags)
        self.setRegularExpression(re)

    def get_regex(self) -> str:
        val = self.regularExpression()
        return val.pattern()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.LineEdit()
    val = RegularExpressionValidator()
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.exec_()
