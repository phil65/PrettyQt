from __future__ import annotations

from prettyqt import location


class PlaceResult(location.PlaceSearchResultMixin, location.QPlaceResult):
    """Represents a search result containing a place."""

    def get_place(self) -> location.Place:
        return location.Place(self.place())
