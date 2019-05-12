# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from prettyqt import gui


class PathValidator(gui.Validator):

    def __repr__(self):
        return "PathValidator()"

    def __getstate__(self):
        return dict()

    def __setstate__(self, state):
        self.__init__()

    def validate(self, text: str, pos: int = 0):
        if pathlib.Path(text).exists():
            return (self.Acceptable, text, pos)
        return (self.Intermediate, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets
    val = PathValidator()
    app = widgets.Application.create_default_app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
