from __future__ import annotations

from prettyqt import location


class PlaceProposedSearchResult(
    location.PlaceSearchResultMixin, location.QPlaceProposedSearchResult
):
    """Represents a search result containing a proposed search."""
