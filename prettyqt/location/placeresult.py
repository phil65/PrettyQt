from __future__ import annotations

from prettyqt import location


class PlaceResult(location.PlaceSearchResultMixin, location.QPlaceResult):
    def get_place(self) -> location.Place:
        return location.Place(self.place())
