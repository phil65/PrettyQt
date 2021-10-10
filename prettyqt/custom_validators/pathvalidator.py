from __future__ import annotations

import pathlib

from prettyqt import gui


class PathValidator(gui.Validator):
    def __eq__(self, other: object):
        return isinstance(other, PathValidator)

    def validate(self, text: str, pos: int = 0):
        if pathlib.Path(text).exists():
            return self.State.Acceptable, text, pos
        return self.State.Intermediate, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = PathValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
