# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets, core
from prettyqt.utils import bidict


ECHO_MODES = bidict(normal=QtWidgets.QLineEdit.Normal,
                    no_echo=QtWidgets.QLineEdit.NoEcho,
                    password=QtWidgets.QLineEdit.Password,
                    echo_on_edit=QtWidgets.QLineEdit.PasswordEchoOnEdit)


QtWidgets.QLineEdit.__bases__ = (widgets.Widget,)


class LineEdit(QtWidgets.QLineEdit):

    value_changed = core.Signal(str)

    def __init__(self, default_value="", read_only=False, parent=None):
        super().__init__(default_value, parent)
        self.textChanged.connect(self.set_validation_color)
        self.textChanged.connect(self.value_changed)
        self.set_read_only(read_only)

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
        self.__init__()
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])
        self.setValidator(state["validator"])
        self.setInputMask(state["input_mask"])
        self.setMaxLength(state["max_length"])
        self.setPlaceholderText(state["placeholder_text"])
        self.setReadOnly(state["read_only"])
        self.setFrame(state["has_frame"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    def font(self) -> gui.Font:
        return gui.Font(super().font())

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

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegExpValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def set_range(self, lower, upper):
        val = gui.IntValidator()
        val.setRange(lower, upper)
        self.set_validator(val)

    def set_validator(self, validator: gui.Validator):
        self.setValidator(validator)
        self.set_validation_color()

    def set_input_mask(self, mask: str):
        self.setInputMask(mask)

    def set_validation_color(self, state: bool = True):
        color = "rgb(255, 175, 90)" if not self.is_valid() else "white"
        self.set_background_color(color)

    def set_echo_mode(self, mode: str):
        """set echo mode

        Valid values are "normal", "no_echo", "password", "echo_on_edit"

        Args:
            policy: echo mode to use

        Raises:
            ValueError: invalid echo mode
        """
        if mode not in ECHO_MODES:
            raise ValueError("Invalid echo mode")
        self.setEchoMode(ECHO_MODES[mode])

    def get_echo_mode(self) -> str:
        """returns echo mode

        possible values are "normal", "no_echo", "password", "echo_on_edit"

        Returns:
            echo mode
        """
        return ECHO_MODES.inv[self.echoMode()]

    def set_value(self, value: str):
        self.setText(value)

    def get_value(self) -> str:
        return self.text()

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()


if __name__ == "__main__":
    app = widgets.app()
    widget = LineEdit("This is a test")
    widget.set_regex_validator("[0-9]+")
    widget.setFont(gui.Font("Consolas"))
    widget.show()
    app.exec_()
