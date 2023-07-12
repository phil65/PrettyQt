from __future__ import annotations

import re

from prettyqt import core, gui
from prettyqt.utils import datatypes, get_repr


class RegularExpressionValidator(gui.ValidatorMixin, gui.QRegularExpressionValidator):
    """Used to check a string against a regular expression."""

    ID = "regular_expression"

    def __init__(self, *args, **kwargs):
        # allow passing strings as well as re.Pattern to the ctor
        match args, kwargs:
            case (str() as pat, *rest), _:
                super().__init__(core.QRegularExpression(pat), *rest, **kwargs)
            case _, {"regular_expression": str() as reg_str, **rest}:
                pat = core.QRegularExpression(reg_str)
                super().__init__(*args, regular_expression=pat, **rest)
            case (re.Pattern() as pat,), _:
                super().__init__(core.RegularExpression(pat))
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

    def set_regex(
        self,
        regex: datatypes.PatternAndStringType,
        flags=None,
    ):
        self.setRegularExpression(datatypes.to_regular_expression(regex))

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
    app.exec()
