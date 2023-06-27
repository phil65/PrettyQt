from __future__ import annotations


try:  # pragma: no cover
    import re._constants as sre_constants
except ImportError:  # Python < 3.11
    import sre_constants  # type: ignore

import re

from prettyqt import core, gui
from prettyqt.utils import get_repr


class RegexPatternValidator(gui.Validator):
    ID = "regex_pattern"
    error_occured = core.Signal(str)
    pattern_updated = core.Signal(object)

    def __repr__(self):
        return get_repr(self)

    def __eq__(self, other: object):
        return isinstance(other, type(self))

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        # if text == "":
        #     self.compiled = None
        #     return (self.Intermediate, text, pos)
        try:
            compiled = re.compile(text)
        except sre_constants.error as e:
            self.error_occured.emit(str(e))
            self.pattern_updated.emit(None)
            return self.State.Intermediate, text, pos
        else:
            self.error_occured.emit("")
            self.pattern_updated.emit(compiled)
            return self.State.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.LineEdit()
    val = RegexPatternValidator()
    w.set_validator(val)
    w.show()
    app.exec()
