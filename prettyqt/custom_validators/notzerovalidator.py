# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui


class NotZeroValidator(gui.Validator):

    def __repr__(self):
        return "NotZeroValidator()"

    def __getstate__(self):
        return dict()

    def __setstate__(self, state):
        self.__init__()

    def validate(self, text, pos=0):
        if text == "0":
            return (self.Intermediate, text, pos)
        return (self.Acceptable, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets
    val = NotZeroValidator()
    app = widgets.Application.create_default_app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
