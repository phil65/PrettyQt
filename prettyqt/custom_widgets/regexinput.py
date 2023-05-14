from __future__ import annotations

from re import Pattern


try:  # pragma: no cover
    import re._constants as sre_constants
except ImportError:  # Python < 3.11
    import sre_constants  # type: ignore

import regex as re

from prettyqt import core, custom_widgets, widgets


MAP = dict(
    multiline=re.MULTILINE,
    ignorecase=re.IGNORECASE,
    ascii=re.ASCII,
    dotall=re.DOTALL,
    verbose=re.VERBOSE,
)


class RegexInput(widgets.Widget):
    value_changed = core.Signal(object)

    def __init__(self, show_flags: bool = True, show_error: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.set_layout("grid", margin=0)
        self.label_error = widgets.Label()
        error_color = self.get_palette().get_color("highlight")
        self.label_error.set_color(error_color)

        self.lineedit = custom_widgets.RegexLineEdit()
        self.lineedit.val.error_occured.connect(self.label_error.set_text)
        self.lineedit.val.pattern_updated.connect(self.value_changed)
        self.tb_flags = custom_widgets.BoolDictToolButton(
            text="Flags", icon="mdi.flag-variant-outline"
        )
        self.box[0, 0:1] = self.lineedit
        if show_flags:
            self.box[0, 2] = self.tb_flags
        if show_error:
            self.box[1, 0:2] = self.label_error
        self.tb_flags.value_changed.connect(self._on_value_change)
        dct = dict(
            multiline="MultiLine",
            ignorecase="Ignore case",
            ascii="ASCII-only matching",
            dotall="Dot matches newline",
            verbose="Ignore whitespace",
        )
        self.tb_flags.set_dict(dct)

    def _on_value_change(self):
        try:
            val = self.get_value()
        except (sre_constants.error, re._regex_core.error):
            return
        else:
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
        match value:
            case None:
                self.pattern = ""
                self.compile_flags = 0
            case str():
                self.pattern = value
                self.compile_flags = 0
            case _:
                self.pattern = value.pattern
                self.compile_flags = value.flags

    def get_value(self) -> Pattern:
        return re.compile(self.pattern, self.compile_flags)

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()

    value = core.Property(Pattern, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = RegexInput(show_flags=True, show_error=True)
    widget.show()
    widget.value_changed.connect(print)
    app.main_loop()
