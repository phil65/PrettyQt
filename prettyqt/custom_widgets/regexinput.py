# -*- coding: utf-8 -*-

from typing import Optional, Pattern, Union

from qtpy import QtWidgets
import regex as re

from prettyqt import core, custom_validators, custom_widgets, widgets


class RegexInput(widgets.Widget):

    value_changed = core.Signal()

    def __init__(
        self,
        show_flags: bool = True,
        show_error: bool = True,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        self.set_layout("grid")
        self.lineedit = custom_widgets.SingleLineTextEdit()
        self.lineedit.set_syntaxhighlighter("regex")
        self.tb_flags = custom_widgets.BoolDictToolButton(
            "Flags", icon="mdi.flag-variant-outline"
        )
        self.label_error = widgets.Label()
        self.label_error.set_color("red")
        self.box[0, 0:1] = self.lineedit
        if show_flags:
            self.box[0, 2] = self.tb_flags
        if show_error:
            self.box[1, 0:2] = self.label_error
        val = custom_validators.RegexPatternValidator()
        val.error_occured.connect(self.label_error.set_text)
        self.lineedit.set_validator(val)
        dct = {
            "multiline": "MultiLine",
            "ignorecase": "Ignore case",
            "ascii": "ASCII-only matching",
            "dotall": "Dot matches newline",
            "verbose": "Ignore whitespace",
        }
        self._mapping = {
            "ignorecase": re.IGNORECASE,
            "multiline": re.MULTILINE,
            "ascii": re.ASCII,
            "dotall": re.DOTALL,
            "verbose": re.VERBOSE,
        }
        self.tb_flags.set_dict(dct)

    @property
    def pattern(self) -> str:
        return self.lineedit.text()

    @pattern.setter
    def pattern(self, value: str):
        self.lineedit.set_text(value)

    @property
    def compile_flags(self) -> int:
        ret_val = 0
        for identifier, flag in self._mapping.items():
            if self.tb_flags[identifier]:
                ret_val |= flag
        return ret_val

    @compile_flags.setter
    def compile_flags(self, value: int):
        for identifier, flag in self._mapping.items():
            self.tb_flags[identifier] = bool(value & flag)

    def set_value(self, value: Optional[Union[str, Pattern]]):
        if value is None:
            self.pattern = ""
            self.flags = 0
        elif isinstance(value, str):
            self.pattern = value
            self.flags = 0
        else:
            self.pattern = value.pattern
            self.compile_flags = value.flags

    def get_value(self) -> Pattern:
        return re.compile(self.pattern, self.compile_flags)

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()


if __name__ == "__main__":
    app = widgets.app()
    widget = RegexInput(show_flags=True, show_error=True)
    widget.show()
    app.main_loop()
