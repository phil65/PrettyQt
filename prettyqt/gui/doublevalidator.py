from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import get_repr


class DoubleValidator(gui.ValidatorMixin, gui.QDoubleValidator):
    ID = "double"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLocale(core.Locale("en-En"))

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
