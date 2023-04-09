from __future__ import annotations

from typing import Literal

from prettyqt import location, positioning
from prettyqt.qt import QtLocation, QtPositioning
from prettyqt.utils import InvalidParamError, bidict


RELEVANCE_HINT = bidict(
    unspecified=QtLocation.QPlaceSearchRequest.UnspecifiedHint,
    distance=QtLocation.QPlaceSearchRequest.DistanceHint,
    lexical_place_name=QtLocation.QPlaceSearchRequest.LexicalPlaceNameHint,
)

RelevanceHintStr = Literal["unspecified", "distance", "lexical_place_name"]


class PlaceSearchRequest(QtLocation.QPlaceSearchRequest):
    def get_visibility_scope(self) -> location.VisibilityStr:
        """Return the scope of the visibility.

        Returns:
            Visibility scope
        """
        return location.VISIBILITY.inverse[self.visibilityScope()]

    def get_categories(self) -> list[location.PlaceCategory]:
        return [location.PlaceCategory(i) for i in self.categories()]

    def get_search_area(self) -> positioning.GeoShape:
        area = self.searchArea()
        match area:
            case QtPositioning.QGeoCircle():
                return positioning.GeoCircle(area)
            case QtPositioning.QGeoPath():
                return positioning.GeoPath(area)
            case QtPositioning.QGeoPolygon():
                return positioning.GeoPolygon(area)
            case QtPositioning.QGeoRectangle():
                return positioning.GeoRectangle(area)
            case _:
                return positioning.GeoShape(area)

    def set_relevance_hint(self, hint: RelevanceHintStr):
        """Set the relevance hint.

        Args:
            hint: Relevance hint

        Raises:
            InvalidParamError: relevance hint does not exist
        """
        if hint not in RELEVANCE_HINT:
            raise InvalidParamError(hint, RELEVANCE_HINT)
        self.setRelevanceHint(RELEVANCE_HINT[hint])

    def get_relevance_hint(self) -> RelevanceHintStr:
        """Return current relevance hint.

        Returns:
            Relevance hint
        """
        return RELEVANCE_HINT.inverse[self.relevanceHint()]


if __name__ == "__main__":
    request = PlaceSearchRequest()
    request.setVisibilityScope("tse")
    print(dir(request))
