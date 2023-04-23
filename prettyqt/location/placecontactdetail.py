from __future__ import annotations

from prettyqt.qt import QtLocation
from prettyqt.utils import get_repr


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
            self.setLabel(other_or_label or "")
            self.setValue(value or "")

    def __repr__(self):
        return get_repr(self, self.label(), self.value())

    def __str__(self):
        return f"{self.label()}: {self.value()}"


if __name__ == "__main__":
    detail = PlaceContactDetail("a", "b")
    print(repr(detail))
