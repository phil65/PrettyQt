from __future__ import annotations

import sre_constants

import regex as re

from prettyqt import core, gui
from prettyqt.qt import QtGui


class RegexPatternValidator(gui.Validator):
    error_occured = core.Signal(str)
    pattern_updated = core.Signal(object)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __eq__(self, other: object):
        return isinstance(other, type(self))

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        # if text == "":
        #     self.compiled = None
        #     return (self.Intermediate, text, pos)
        try:
            compiled = re.compile(text)
        except sre_constants.error as e:
            self.error_occured.emit(str(e))
            self.pattern_updated.emit(None)
            return self.State.Intermediate, text, pos
        except re._regex_core.error as e:
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
    app.main_loop()
