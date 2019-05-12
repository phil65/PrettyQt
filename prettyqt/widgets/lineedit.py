# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets, core

ECHO_MODES = dict(normal=QtWidgets.QLineEdit.Normal,
                  no_echo=QtWidgets.QLineEdit.NoEcho,
                  password=QtWidgets.QLineEdit.Password,
                  echo_on_edit=QtWidgets.QLineEdit.PasswordEchoOnEdit)


class LineEdit(QtWidgets.QLineEdit):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.set_validation_color)
        self.textChanged.connect(self.value_changed)

    def __repr__(self):
        return f"LineEdit: {self.__getstate__()}"

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    font=gui.Font(self.font()),
                    validator=self.validator(),
                    max_length=self.maxLength(),
                    read_only=self.isReadOnly(),
                    input_mask=self.inputMask(),
                    has_frame=self.hasFrame(),
                    placeholder_text=self.placeholderText())

    def __setstate__(self, state):
        super().__init__()
        self.set_text(state["text"])
        self.setEnabled(state["enabled"])
        self.setFont(state["font"])
        self.setValidator(state["validator"])
        self.setInputMask(state["input_mask"])
        self.setMaxLength(state["max_length"])
        self.setPlaceholderText(state["placeholder_text"])
        self.setReadOnly(state["read_only"])
        self.setFrame(state["has_frame"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def font(self) -> gui.Font:
        return gui.Font(super().font())

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

    def append_text(self, text: str):
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

    def set_input_mask(self, mask: str):
        self.setInputMask(mask)

    def set_color(self, color: str):
        self.setStyleSheet(f"background-color: {color};")

    def set_validation_color(self, state: bool):
        color = "rgb(255, 175, 90)" if not self.is_valid() else "white"
        self.set_color(color)

    def set_echo_mode(self, mode: str):
        self.setEchoMode(ECHO_MODES[mode])

    def set_value(self, value: str):
        self.setText(value)

    def get_value(self) -> str:
        return self.text()

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = LineEdit("This is a test")
    widget.set_regex_validator("[0-9]+")
    widget.setFont(gui.Font("Consolas"))
    widget.show()
    app.exec_()
