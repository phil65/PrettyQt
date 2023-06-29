from __future__ import annotations

from typing import Literal
import pathlib

from prettyqt import core, gui

ModeStr = Literal["any", "file", "folder"]


class PathValidator(gui.Validator):
    """Validator which checks whether given string is a valid path."""

    ID = "path"

    def __init__(self, *args, **kwargs):
        self._mode = "any"
        super().__init__(*args, **kwargs)

    def __eq__(self, other: object):
        return isinstance(other, PathValidator) and self._mode == other._mode

    def validate(self, text: str, pos: int = 0):
        path = pathlib.Path(text)
        if not path.exists():
            return self.State.Intermediate, text, pos
        match self._mode:
            case "any":
                return self.State.Acceptable, text, pos
            case "file" if path.is_file():
                return self.State.Acceptable, text, pos
            case "folder" if path.is_dir():
                return self.State.Acceptable, text, pos
        return self.State.Intermediate, text, pos

    def set_mode(self, mode: ModeStr):
        self._mode = mode

    def get_mode(self) -> ModeStr:
        return self._mode

    mode = core.Property(str, get_mode, set_mode)


if __name__ == "__main__":
    from prettyqt import widgets

    val = PathValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec()
