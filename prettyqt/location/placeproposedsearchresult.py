from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceProposedSearchResult.__bases__ = (location.PlaceSearchResult,)


class PlaceProposedSearchResult(QtLocation.QPlaceProposedSearchResult):
    pass
