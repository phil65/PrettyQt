from typing import TYPE_CHECKING, Literal

from prettyqt import location
from prettyqt.utils import bidict


TYPE = bidict(
    unknown=location.QPlaceSearchResult.SearchResultType.UnknownSearchResult,
    place=location.QPlaceSearchResult.SearchResultType.PlaceResult,
    proposed_search=location.QPlaceSearchResult.SearchResultType.ProposedSearchResult,
)

TypeStr = Literal["unknown", "place", "proposed_search"]


if TYPE_CHECKING:
    from prettyqt.qt import QtLocation

    _PlaceSearchResultBase = QtLocation.QPlaceSearchResult
else:
    _PlaceSearchResultBase = object


class PlaceSearchResultMixin(_PlaceSearchResultBase):
    def get_icon(self) -> location.PlaceIcon | None:
        icon = self.icon()
        return None if icon.isEmpty() else location.PlaceIcon(icon)

    def get_type(self) -> TypeStr:
        """Return result type.

        Returns:
            Result type
        """
        return TYPE.inverse[self.type()]


class PlaceSearchResult(PlaceSearchResultMixin, location.QPlaceSearchResult):
    """The base class for search results."""
