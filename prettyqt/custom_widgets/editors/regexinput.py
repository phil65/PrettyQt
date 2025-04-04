from __future__ import annotations

import enum
import re
from re import Pattern
import re._constants as sre_constants
from typing import ClassVar

from prettyqt import core, custom_widgets, widgets


class RegexFlag(enum.IntEnum):
    NOFLAG = 0
    ASCII = 256  # assume ascii "locale"
    IGNORECASE = 2  # ignore case
    LOCALE = 4  # assume current 8-bit locale
    UNICODE = 32  # assume unicode "locale"
    MULTILINE = 8  # make anchors look for newline
    DOTALL = 16  # make dot match newline
    VERBOSE = 64  # ignore whitespace and comments
    # sre extensions (experimental, don't rely on these)
    TEMPLATE = 1  # unknown purpose, deprecated
    DEBUG = 128  # dump pattern after compilation


class RegexInput(widgets.Widget):
    LABEL_MAP: ClassVar = dict(
        multiline="MultiLine",
        ignorecase="Ignore case",
        ascii="ASCII-only matching",
        dotall="Dot matches newline",
        verbose="Ignore whitespace",
    )
    VALUE_MAP: ClassVar = dict(
        multiline=re.MULTILINE,
        ignorecase=re.IGNORECASE,
        ascii=re.ASCII,
        dotall=re.DOTALL,
        verbose=re.VERBOSE,
    )
    Flags = RegexFlag
    core.Enum(Flags)

    value_changed = core.Signal(object)

    def __init__(
        self,
        show_flags: bool = True,
        show_error: bool = True,
        object_name: str = "regex_input",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        self.set_layout("grid", margin=0)
        self.label_error = widgets.Label()
        self.label_error.set_color("highlight_role")
        self.lineedit = custom_widgets.RegexLineEdit()
        val = self.lineedit.validator
        val.error_occured.connect(self.label_error.set_text)
        val.pattern_updated.connect(self.value_changed)
        self.tb_flags = custom_widgets.BoolDictToolButton(
            text="Flags", icon="mdi.flag-variant-outline"
        )
        self.box[0, 0:1] = self.lineedit
        if show_flags:
            self.box[0, 2] = self.tb_flags
        if show_error:
            self.box[1, 0:2] = self.label_error
        self.tb_flags.value_changed.connect(self._on_value_change)

        self.tb_flags.set_dict(self.LABEL_MAP)

    def _on_value_change(self):
        try:
            val = self.get_value()
        except sre_constants.error:
            return
        else:
            self.value_changed.emit(val)

    def get_pattern(self) -> str:
        return self.lineedit.text()

    def set_pattern(self, value: str):
        self.lineedit.set_text(value)

    def get_flags(self) -> int:
        ret_val = self.Flags(0)
        for identifier, flag in self.VALUE_MAP.items():
            if self.tb_flags[identifier]:
                ret_val |= flag
        return ret_val

    def set_flags(self, value: int):
        for identifier, flag in self.VALUE_MAP.items():
            self.tb_flags[identifier] = bool(value & flag)

    def set_value(self, value: str | Pattern | None):
        match value:
            case None:
                self.set_pattern("")
                self.set_flags(self.Flags(0))
            case str():
                self.set_pattern(value)
                self.set_flags(self.Flags(0))
            case _:
                self.set_pattern(value.pattern)
                self.set_flags(self.Flags(value.flags))

    def get_value(self) -> Pattern:
        return re.compile(self.get_pattern(), self.get_flags())

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()

    pattern = core.Property(
        str,
        get_pattern,
        set_pattern,
        user=True,
        doc="Current pattern as text",
    )
    # flags = core.Property(Flags, get_flags, set_flags)


if __name__ == "__main__":
    app = widgets.app()
    widget = RegexInput(show_flags=True, show_error=True)
    table = widgets.TableView()
    table.set_delegate("editor")
    table.set_model_for(widget)
    table.show()
    widget.show()
    widget.value_changed.connect(print)
    with app.debug_mode():
        app.exec()
