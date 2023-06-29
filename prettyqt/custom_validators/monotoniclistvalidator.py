from __future__ import annotations

import re

from prettyqt import gui

re_custom_sep = re.compile(r"\s*,\s*")


class MonotonicListValidator(gui.Validator):
    """Validator which checks whether given string contains a monotonic list."""

    ID = "monotonic"

    def __init__(self, kind: str = "increasing", parent=None):
        super().__init__(parent)
        self._kind = kind

    def __eq__(self, other: object):
        return isinstance(other, MonotonicListValidator) and other._kind == self._kind

    def validate(self, string: str, pos: int) -> tuple[gui.Validator.State, str, int]:
        if self._kind != "increasing":
            string = string[::-1]
        for i, c in enumerate(string, start=1):
            if c not in "+-., 0123456789":
                return self.State.Invalid, string, i
        if pos == len(string) >= 2 and string[-1] == " " and string[-2].isdigit():
            string = f"{string[:-1]}, "
            pos += 1
        prev = None
        for valuestr in re_custom_sep.split(string.strip()):
            try:
                value = float(valuestr)
            except ValueError:
                return self.State.Intermediate, string, pos
            if prev is not None and value <= prev:
                return self.State.Intermediate, string, pos
            prev = value
        return self.State.Acceptable, string, pos


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = MonotonicListValidator(kind="decreasing")
    print(val.validate("1,0", 0))
