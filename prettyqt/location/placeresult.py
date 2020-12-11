from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceResult.__bases__ = (location.PlaceSearchResult,)


class PlaceResult(QtLocation.QPlaceResult):
    def get_place(self) -> location.Place:
        return location.Place(self.place())
