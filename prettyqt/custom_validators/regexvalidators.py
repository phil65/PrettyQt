# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui


class IntListValidator(gui.RegExpValidator):

    def __repr__(self):
        return f"IntListValidator(allow_single={self.allow_single})"

    def __init__(self, allow_single=True, parent=None):
        super().__init__(parent)
        self.allow_single = allow_single
        if allow_single:
            self.set_regex(r"^(\d+)(,\s*\d+)*$")
        else:
            self.set_regex(r"^[0-9][0-9\,]+[0-9]$")


class FloatListValidator(gui.RegExpValidator):

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
