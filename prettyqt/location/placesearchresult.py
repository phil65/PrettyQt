from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


TYPE = bidict(
    unknown=QtLocation.QPlaceSearchResult.UnknownSearchResult,
    place=QtLocation.QPlaceSearchResult.PlaceResult,
    proposed_search=QtLocation.QPlaceSearchResult.ProposedSearchResult,
)

TypeStr = Literal["unknown", "place", "proposed_search"]


class PlaceSearchResult(QtLocation.QPlaceSearchResult):
    def get_icon(self) -> location.PlaceIcon | None:
        icon = self.icon()
        if icon.isEmpty():
            return None
        return location.PlaceIcon(icon)

    def get_type(self) -> TypeStr:
        """Return result type.

        Returns:
            Result type
        """
        return TYPE.inverse[self.type()]
