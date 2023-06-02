from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import get_repr


class RegularExpressionValidator(gui.ValidatorMixin, QtGui.QRegularExpressionValidator):
    ID = "regular_expression"

    def __init__(self, *args, **kwargs):
        match args, kwargs:
            case (str(), *rest), _:
                super().__init__(QtCore.QRegularExpression(args[0]), *rest, **kwargs)
            case _, {"regular_expression": str() as reg_str, **rest}:
                super().__init__(
                    *args,
                    regular_expression=QtCore.QRegularExpression(reg_str),
                    **rest,
                )
            case _, _:
                super().__init__(*args, **kwargs)

    def __repr__(self):
        return get_repr(self, self.regularExpression())

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
    val = RegularExpressionValidator("test")
    val.set_regex(r"\w\d\d")
    w.set_validator(val)
    w.show()
    app.main_loop()
