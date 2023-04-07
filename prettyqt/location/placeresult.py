from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


class PlaceResult(location.PlaceSearchResultMixin, QtLocation.QPlaceResult):
    def get_place(self) -> location.Place:
        return location.Place(self.place())
