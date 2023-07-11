from __future__ import annotations

from typing import Literal

from prettyqt import location, positioning
from prettyqt.utils import bidict


RelevanceHintStr = Literal["unspecified", "distance", "lexical_place_name"]

RELEVANCE_HINT: bidict[RelevanceHintStr, location.QPlaceSearchRequest.RelevanceHint] = (
    bidict(
        unspecified=location.QPlaceSearchRequest.RelevanceHint.UnspecifiedHint,
        distance=location.QPlaceSearchRequest.RelevanceHint.DistanceHint,
        lexical_place_name=location.QPlaceSearchRequest.RelevanceHint.LexicalPlaceNameHint,
    )
)


class PlaceSearchRequest(location.QPlaceSearchRequest):
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
            case positioning.QGeoCircle():
                return positioning.GeoCircle(area)
            case positioning.QGeoPath():
                return positioning.GeoPath(area)
            case positioning.QGeoPolygon():
                return positioning.GeoPolygon(area)
            case positioning.QGeoRectangle():
                return positioning.GeoRectangle(area)
            case _:
                return positioning.GeoShape(area)

    def set_relevance_hint(
        self, hint: RelevanceHintStr | location.QPlaceSearchRequest.RelevanceHint
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
