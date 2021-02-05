from __future__ import annotations

from prettyqt import core, location, positioning
from prettyqt.qt import QtLocation, QtPositioning


QtLocation.QPlaceManager.__bases__ = (core.Object,)


class PlaceManager(core.Object):
    on_finished = core.Signal(location.PlaceSearchReply)

    def __init__(self, item: QtLocation.QPlaceManager):
        super().__init__()
        self.item = item
        self.finished.connect(self._on_finished)

    def __getattr__(self, val):
        return getattr(self.item, val)

    def _on_finished(self, reply: QtLocation.QPlaceSearchReply):
        reply = location.PlaceSearchReply.clone_from(reply)
        self.on_finished.emit(reply)

    def get_category(self, cat_id: str) -> location.PlaceCategory:
        return location.PlaceCategory(self.item.category(cat_id))

    def get_child_categories(self, cat_id: str) -> list[location.PlaceCategory]:
        return [location.PlaceCategory(i) for i in self.item.childCategories(cat_id)]

    def get_locales(self) -> list[core.Locale]:
        return [core.Locale(i) for i in self.locales()]

    def search_place(
        self,
        search_term: str,
        coord: tuple[float, float] | QtPositioning.QGeoCoordinate,
        radius: float | None = None,
        limit: int | None = None,
        relevance: location.placesearchrequest.RelevanceHintStr | None = None,
        categories: list[str] | None = None,
    ):
        request = location.PlaceSearchRequest()
        request.setSearchTerm(search_term)
        if radius is None:
            radius = -1
        if isinstance(coord, tuple):
            coord = positioning.GeoCoordinate(*coord)
        circle = positioning.GeoCircle(coord, radius)
        request.setSearchArea(circle)
        if limit is not None:
            request.setLimit(limit)
        if relevance is not None:
            request.set_relevance_hint(relevance)
        if categories is not None:
            self.setCategories(categories)
        return self.search(request)


if __name__ == "__main__":
    app = core.app()
    provider = location.GeoServiceProvider("osm")
    manager = provider.get_place_manager()
    reply = manager.search_place("Shop", coord=(51, 7))
    manager.on_finished.connect(lambda x: print(x.get_results()))
    app.main_loop()
