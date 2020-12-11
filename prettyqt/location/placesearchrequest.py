from typing import List

from qtpy import QtLocation, PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning


from prettyqt import location, positioning
from prettyqt.utils import bidict, InvalidParamError

RELEVANCE_HINT = bidict(
    unspecified=QtLocation.QPlaceSearchRequest.UnspecifiedHint,
    distance=QtLocation.QPlaceSearchRequest.DistanceHint,
    lexical_place_name=QtLocation.QPlaceSearchRequest.LexicalPlaceNameHint,
)

VISIBILITY = bidict(
    unspecified=QtLocation.QLocation.UnspecifiedVisibility,
    device=QtLocation.QLocation.DeviceVisibility,
    private=QtLocation.QLocation.PrivateVisibility,
    public=QtLocation.QLocation.PublicVisibility,
)


class PlaceSearchRequest(QtLocation.QPlaceSearchRequest):
    def get_visibility_scope(self) -> str:
        """Return the scope of the visibility.

        Possible values are "unspecified", "device", "private", "public"

        Returns:
            Visibility scope
        """
        return VISIBILITY.inv[self.visibilityScope()]

    def get_categories(self) -> List[location.PlaceCategory]:
        return [location.PlaceCategory(i) for i in self.categories()]

    def get_search_area(self) -> positioning.GeoShape:
        area = self.searchArea()
        if isinstance(area, QtPositioning.QGeoCircle):
            return positioning.GeoCircle(area)
        elif isinstance(area, QtPositioning.QGeoPath):
            return positioning.GeoPath(area)
        elif isinstance(area, QtPositioning.QGeoPolygon):
            return positioning.GeoPolygon(area)
        elif isinstance(area, QtPositioning.QGeoRectangle):
            return positioning.GeoRectangle(area)
        else:
            return positioning.GeoShape(area)

    def set_relevance_hint(self, hint: str):
        """Set the relevance hint.

        Allowed values are "unspecified", "distance", "lexical_place_name"

        Args:
            hint: Relevance hint

        Raises:
            InvalidParamError: relevance hint does not exist
        """
        if hint not in RELEVANCE_HINT:
            raise InvalidParamError(hint, RELEVANCE_HINT)
        self.setRelevanceHint(RELEVANCE_HINT[hint])

    def get_relevance_hint(self) -> str:
        """Return current relevance hint.

        Possible values: "unspecified", "distance", "lexical_place_name"

        Returns:
            Relevance hint
        """
        return RELEVANCE_HINT.inv[self.relevanceHint()]


if __name__ == "__main__":
    request = PlaceSearchRequest()
    print(bool(request))
