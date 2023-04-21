from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


TYPE = bidict(
    unknown=QtLocation.QPlaceSearchResult.SearchResultType.UnknownSearchResult,
    place=QtLocation.QPlaceSearchResult.SearchResultType.PlaceResult,
    proposed_search=QtLocation.QPlaceSearchResult.SearchResultType.ProposedSearchResult,
)

TypeStr = Literal["unknown", "place", "proposed_search"]


class PlaceSearchResultMixin:
    def get_icon(self) -> location.PlaceIcon | None:
        icon = self.icon()
        return None if icon.isEmpty() else location.PlaceIcon(icon)

    def get_type(self) -> TypeStr:
        """Return result type.

        Returns:
            Result type
        """
        return TYPE.inverse[self.type()]


class PlaceSearchResult(PlaceSearchResultMixin, QtLocation.QPlaceSearchResult):
    pass
