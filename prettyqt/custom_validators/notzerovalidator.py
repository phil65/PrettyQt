# -*- coding: utf-8 -*-
"""
"""

from prettyqt import gui


class NotZeroValidator(gui.Validator):
    def __getstate__(self):
        return dict()

    def __setstate__(self, state):
        self.__init__()

    def validate(self, text: str, pos: int = 0) -> tuple:
        if text == "0":
            return (self.Intermediate, text, pos)
        return (self.Acceptable, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets

    val = NotZeroValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
