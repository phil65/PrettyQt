from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


QtLocation.QPlaceResult.__bases__ = (location.PlaceSearchResult,)


class PlaceResult(QtLocation.QPlaceResult):
    def get_place(self) -> location.Place:
        return location.Place(self.place())
