from typing import Literal

from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import bidict


TYPE = bidict(
    unknown=QtLocation.QPlaceSearchResult.UnknownSearchResult,
    place=QtLocation.QPlaceSearchResult.PlaceResult,
    proposed_search=QtLocation.QPlaceSearchResult.ProposedSearchResult,
)

TypeStr = Literal["unknown", "place", "proposed_search"]


class PlaceSearchResult(QtLocation.QPlaceSearchResult):
    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def get_type(self) -> TypeStr:
        """Return result type.

        Returns:
            Result type
        """
        return TYPE.inverse[self.type()]
