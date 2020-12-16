from typing import Iterator, List, Optional

from qtpy import QtCore

from prettyqt import gui


class CompositeValidator(gui.Validator):
    def __init__(
        self,
        validators: Optional[List[gui.Validator]] = None,
        parent: Optional[QtCore.QObject] = None,
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
        return self.__class__, (self.validators,)

    def __len__(self):
        return len(self.validators)

    def __eq__(self, other: object):
        if not isinstance(other, type(self)):
            return False
        return self.validators == other.validators

    def validate(self, text: str, pos: int = 0) -> tuple:
        vals = [v.validate(text, pos)[0] for v in self.validators]
        return min(vals), text, pos


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
