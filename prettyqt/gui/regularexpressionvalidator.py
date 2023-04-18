from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


class RegularExpressionValidator(gui.ValidatorMixin, QtGui.QRegularExpressionValidator):
    def __repr__(self):
        return f"{type(self).__name__}(RegularExpression({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(pattern=core.RegularExpression(self.regularExpression()))

    def __setstate__(self, state):
        self.setRegularExpression(state["pattern"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __eq__(self, other: object):
        return (
            self.regularExpression() == other.regularExpression()
            if isinstance(other, type(self))
            else False
        )

    def set_regex(self, regex: str | core.RegularExpression, flags=0):
        if isinstance(regex, str):
            regex = core.RegularExpression(regex, flags)
        self.setRegularExpression(regex)

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
    app.main_loop()
