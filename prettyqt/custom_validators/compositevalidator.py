from __future__ import annotations

from collections.abc import Iterator

from prettyqt import gui
from prettyqt.qt import QtCore, QtGui


class CompositeValidator(gui.Validator):
    def __init__(
        self,
        validators: list[gui.Validator] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self.validators = validators if validators is not None else []

    def __repr__(self):
        return f"{type(self).__name__}({self.validators})"

    def __getitem__(self, index: int) -> gui.Validator:
        return self.validators[index]

    def __setitem__(self, index: int, value: gui.Validator):
        self.validators[index] = value

    def __delitem__(self, index: int):
        del self.validators[index]

    def __contains__(self, index: int):
        return index in self.validators

    def __iter__(self) -> Iterator[gui.Validator]:
        return iter(self.validators)

    def __reduce__(self):
        return type(self), (self.validators,)

    def __len__(self):
        return len(self.validators)

    def __eq__(self, other: object):
        if not isinstance(other, type(self)):
            return False
        return self.validators == other.validators

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[QtGui.QValidator.State, str, int]:
        vals = [v.validate(text, pos)[0] for v in self.validators]  # type: ignore
        if self.State.Invalid in vals:
            return self.State.Invalid, text, pos
        elif self.State.Intermediate in vals:
            return self.State.Intermediate, text, pos
        else:
            return self.State.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import custom_validators, widgets

    val1 = custom_validators.NotEmptyValidator()
    val2 = custom_validators.PathValidator()
    val = CompositeValidator([val1, val2])
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
