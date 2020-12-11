from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import bidict

TYPE = bidict(
    unknown=QtLocation.QPlaceSearchResult.UnknownSearchResult,
    place=QtLocation.QPlaceSearchResult.PlaceResult,
    proposed_search=QtLocation.QPlaceSearchResult.ProposedSearchResult,
)


class PlaceSearchResult(QtLocation.QPlaceSearchResult):
    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def get_type(self) -> str:
        """Return result type.

        possible values: "unknown" "place", "proposed_search",

        Returns:
            Result type
        """
        return TYPE.inverse[self.type()]
