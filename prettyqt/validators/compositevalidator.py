from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import gui
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from prettyqt.qt import QtCore


class CompositeValidator(gui.Validator):
    """BaseClass for combined validators."""

    ID = "composite"

    def __init__(
        self,
        validators: Sequence[gui.Validator] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self.validators = validators if validators is not None else []

    def __repr__(self):
        return get_repr(self, self.validators)

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
        return (
            self.validators == other.validators
            if isinstance(other, type(self))
            else False
        )

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        return NotImplemented


class AndValidator(CompositeValidator):
    """Validator to AND-combine other validators."""

    ID = "and"

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        vals = [v.validate(text, pos)[0] for v in self.validators]  # type: ignore
        if self.State.Invalid in vals:
            return self.State.Invalid, text, pos
        if self.State.Intermediate in vals:
            return self.State.Intermediate, text, pos
        return self.State.Acceptable, text, pos


class OrValidator(CompositeValidator):
    """Validator to OR-combine other validators."""

    ID = "or"

    def validate(  # type: ignore
        self, text: str, pos: int = 0
    ) -> tuple[gui.QValidator.State, str, int]:
        vals = [v.validate(text, pos)[0] for v in self.validators]  # type: ignore
        if self.State.Acceptable in vals:
            return self.State.Acceptable, text, pos
        if self.State.Intermediate in vals:
            return self.State.Intermediate, text, pos
        return self.State.Invalid, text, pos


if __name__ == "__main__":
    from prettyqt import validators, widgets

    val1 = validators.NotEmptyValidator()
    val2 = validators.PathValidator()
    val = AndValidator([val1, val2])
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec()
