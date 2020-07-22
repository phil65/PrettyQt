# -*- coding: utf-8 -*-
"""
"""

import sre_constants
from typing import Optional

from qtpy import QtCore
import regex as re

from prettyqt import gui


class RegexPatternValidator(gui.Validator):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)
        self.error_message = ""
        self.compiled = None

    def __repr__(self):
        return "RegexPatternValidator()"

    def validate(self, text: str, pos: int = 0) -> tuple:
        # if text == "":
        #     self.compiled = None
        #     return (self.Intermediate, text, pos)
        try:
            self.compiled = re.compile(text)
        except sre_constants.error as e:
            self.error_message = str(e)
            self.compiled = None
            return (self.Intermediate, text, pos)
        except re._regex_core.error as e:
            self.error_message = str(e)
            self.compiled = None
            return (self.Intermediate, text, pos)
        else:
            self.error_message = ""
            return (self.Acceptable, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.LineEdit()
    val = RegexPatternValidator()
    w.set_validator(val)
    w.show()
    app.exec_()
