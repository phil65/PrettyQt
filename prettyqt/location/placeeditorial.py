from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


QtLocation.QPlaceEditorial.__bases__ = (location.PlaceContent,)


class PlaceEditorial(QtLocation.QPlaceEditorial):
    def __str__(self):
        return f"{self.title()}: {self.text()}"


if __name__ == "__main__":
    editorial = PlaceEditorial()
