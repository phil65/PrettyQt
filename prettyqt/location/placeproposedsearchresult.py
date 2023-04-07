from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


class PlaceProposedSearchResult(
    location.PlaceSearchResultMixin, QtLocation.QPlaceProposedSearchResult
):
    pass
