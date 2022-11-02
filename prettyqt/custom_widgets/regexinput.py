from __future__ import annotations

from re import Pattern

import regex as re

from prettyqt import core, custom_validators, custom_widgets, widgets
from prettyqt.qt import QtWidgets


MAP = dict(
    multiline=re.MULTILINE,
    ignorecase=re.IGNORECASE,
    ascii=re.ASCII,
    dotall=re.DOTALL,
    verbose=re.VERBOSE,
)


class RegexInput(widgets.Widget):

    value_changed = core.Signal(object)

    def __init__(
        self,
        show_flags: bool = True,
        show_error: bool = True,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.set_layout("grid")
        self.lineedit = custom_widgets.SingleLineTextEdit()
        self.lineedit.set_syntaxhighlighter("regex")
        self.tb_flags = custom_widgets.BoolDictToolButton(
            "Flags", icon="mdi.flag-variant-outline"
        )
        self.label_error = widgets.Label()
        error_color = self.get_palette().get_color("highlight")
        self.label_error.set_color(error_color)
        self.box[0, 0:1] = self.lineedit
        if show_flags:
            self.box[0, 2] = self.tb_flags
        if show_error:
            self.box[1, 0:2] = self.label_error
        val = custom_validators.RegexPatternValidator()
        val.error_occured.connect(self.label_error.set_text)
        val.pattern_updated.connect(self.value_changed)
        self.tb_flags.value_changed.connect(self._on_value_change)
        self.lineedit.set_validator(val)
        dct = dict(
            multiline="MultiLine",
            ignorecase="Ignore case",
            ascii="ASCII-only matching",
            dotall="Dot matches newline",
            verbose="Ignore whitespace",
        )
        self.tb_flags.set_dict(dct)

    def _on_value_change(self):
        val = self.get_value()
        self.value_changed.emit(val)

    @property
    def pattern(self) -> str:
        return self.lineedit.text()

    @pattern.setter
    def pattern(self, value: str):
        self.lineedit.set_text(value)

    @property
    def compile_flags(self) -> int:
        ret_val = 0
        for identifier, flag in MAP.items():
            if self.tb_flags[identifier]:
                ret_val |= flag
        return ret_val

    @compile_flags.setter
    def compile_flags(self, value: int):
        for identifier, flag in MAP.items():
            self.tb_flags[identifier] = bool(value & flag)

    def set_value(self, value: str | Pattern | None):
        if value is None:
            self.pattern = ""
            self.compile_flags = 0
        elif isinstance(value, str):
            self.pattern = value
            self.compile_flags = 0
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
    widget.value_changed.connect(print)
    app.main_loop()
