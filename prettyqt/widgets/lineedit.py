# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets


class LineEdit(QtWidgets.QLineEdit):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_font(self,
                 font_name: str,
                 font_size: int = -1,
                 weight: int = -1,
                 italic: bool = False):
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)

    def append(self, text: str):
        self.set_text(self.text() + text)

    def set_text(self, text: str):
        self.setText(text)

    def set_read_only(self, value: bool = True):
        """set test to read only

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def set_regex_validator(self, regex: str) -> gui.RegExpValidator:
        validator = gui.RegExpValidator(self)
        validator.set_regex(regex)
        self.setValidator(validator)
        return validator


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = LineEdit("This is a test")
    widget.show()
    app.exec_()
