from typing import Literal

from prettyqt import core, gui
from prettyqt.utils import bidict, get_repr


NotationStr = Literal["standard", "scientific"]

NOTATION: bidict[NotationStr, gui.QDoubleValidator.Notation] = bidict(
    standard=gui.QDoubleValidator.Notation.StandardNotation,
    scientific=gui.QDoubleValidator.Notation.ScientificNotation,
)


class DoubleValidator(gui.ValidatorMixin, gui.QDoubleValidator):
    """Range checking of floating-point numbers."""

    ID = "double"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLocale(core.Locale("en-En"))

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"notation": NOTATION}
        return maps

    def get_notation(self) -> NotationStr:
        return NOTATION.inverse[self.notation()]

    def set_notation(self, notation: NotationStr | gui.QDoubleValidator.Notation):
        self.setNotation(NOTATION.get_enum_value(notation))

    def __repr__(self):
        return get_repr(self, self.bottom(), self.top(), self.decimals())

    def __reduce__(self):
        return type(self), (self.bottom(), self.top(), self.decimals()), None

    def __eq__(self, other: object):
        return (
            (
                self.bottom() == other.bottom()
                and self.top() == other.top()
                and self.decimals() == other.decimals()
            )
            if isinstance(other, type(self))
            else False
        )

    def set_range(
        self, start: float | None, end: float | None, decimals: int | None = None
    ):
        if decimals is None:
            decimals = -1
        if start is None:
            start = -float("inf")
        if end is None:
            end = float("inf")
        self.setRange(start, end, decimals)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    lineedit = widgets.LineEdit()
    val = DoubleValidator()
    # val.setRange(0, 9)
    lineedit.set_validator(val)
    lineedit.show()
    app.exec()
