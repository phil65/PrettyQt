from __future__ import annotations

from typing import Literal

from prettyqt import location, positioning
from prettyqt.qt import QtLocation, QtPositioning
from prettyqt.utils import bidict


RelevanceHintStr = Literal["unspecified", "distance", "lexical_place_name"]

RELEVANCE_HINT: bidict[
    RelevanceHintStr, QtLocation.QPlaceSearchRequest.RelevanceHint
] = bidict(
    unspecified=QtLocation.QPlaceSearchRequest.RelevanceHint.UnspecifiedHint,
    distance=QtLocation.QPlaceSearchRequest.RelevanceHint.DistanceHint,
    lexical_place_name=QtLocation.QPlaceSearchRequest.RelevanceHint.LexicalPlaceNameHint,
)


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

    def set_relevance_hint(
        self, hint: RelevanceHintStr | QtLocation.QPlaceSearchRequest.RelevanceHint
    ):
        """Set the relevance hint.

        Args:
            hint: Relevance hint
        """
        self.setRelevanceHint(RELEVANCE_HINT.get_enum_value(hint))

    def get_relevance_hint(self) -> RelevanceHintStr:
        """Return current relevance hint.

        Returns:
            Relevance hint
        """
        return RELEVANCE_HINT.inverse[self.relevanceHint()]


if __name__ == "__main__":
    request = PlaceSearchRequest()
    print(dir(request))
