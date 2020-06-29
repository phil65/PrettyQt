# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import regex as re
import sre_constants

from prettyqt import gui


class RegexPatternValidator(gui.Validator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = ""
        self.compiled = None

    def __repr__(self):
        return "RegexPatternValidator()"

    def validate(self, text, pos=0):
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
