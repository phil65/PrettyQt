from __future__ import annotations

from prettyqt.qt import QtLocation


class PlaceContactDetail(QtLocation.QPlaceContactDetail):
    def __init__(
        self,
        other_or_label: None | str | QtLocation.QPlaceAttribute = None,
        value: str | None = None,
    ):
        if isinstance(other_or_label, QtLocation.QPlaceAttribute):
            super().__init__(other_or_label)
        else:
            super().__init__()
            self.setLabel(other_or_label if other_or_label else "")
            self.setValue(value if value else "")

    def __repr__(self):
        return f"{type(self).__name__}({self.label()!r}, {self.value()!r})"

    def __str__(self):
        return f"{self.label()}: {self.value()}"


if __name__ == "__main__":
    detail = PlaceContactDetail("a", "b")
    print(repr(detail))
    print(detail.Email)
