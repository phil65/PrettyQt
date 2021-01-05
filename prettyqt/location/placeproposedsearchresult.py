from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


QtLocation.QPlaceProposedSearchResult.__bases__ = (location.PlaceSearchResult,)


class PlaceProposedSearchResult(QtLocation.QPlaceProposedSearchResult):
    pass
