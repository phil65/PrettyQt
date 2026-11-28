import pathlib
from typing import Literal

from prettyqt import core, gui


ModeStr = Literal["any", "file", "folder"]


class PathValidator(gui.Validator):
    """Validator which checks whether given string is a valid path."""

    ID = "path"

    def __init__(self, *args, **kwargs):
        self._mode: ModeStr = "any"
        super().__init__(*args, **kwargs)

    def __eq__(self, other: object):
        return isinstance(other, PathValidator) and self._mode == other._mode

    def validate(self, text: str, pos: int = 0):
        if not text:
            return self.State.Intermediate, text, pos
        try:
            path = pathlib.Path(text)
            exists = path.exists()
        except ValueError, OSError:
            return self.State.Invalid, text, pos
        if not exists:
            return self.State.Intermediate, text, pos
        match self._mode:
            case "any":
                is_valid = True
            case "file":
                is_valid = path.is_file()
            case "folder":
                is_valid = path.is_dir()
            case _:
                is_valid = False
        state = self.State.Acceptable if is_valid else self.State.Intermediate
        return state, text, pos

    def set_mode(self, mode: ModeStr):
        self._mode = mode

    def get_mode(self) -> ModeStr:
        return self._mode

    mode = core.Property(
        str,
        get_mode,
        set_mode,
        doc="Whether text can be any, an existing file or an existing folder",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    val = PathValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec()
