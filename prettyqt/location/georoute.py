from __future__ import annotations

from prettyqt import location, positioning
from prettyqt.qt import QtLocation
from prettyqt.utils import types


class GeoRoute(QtLocation.QGeoRoute):
    def __setitem__(self, index: str, val: types.Variant):
        attrs = self.extendedAttributes()
        attrs[index] = val
        self.setExtendedAttributes(attrs)

    def __getitem__(self, index: str) -> types.Variant:
        attr = self.extendedAttributes()
        if index not in attr:
            raise KeyError(f"Key {index!r} does not exist.")
        return attr[index]

    def __abs__(self) -> float:
        return self.distance()

    def get_bounds(self) -> positioning.GeoRectangle:
        return positioning.GeoRectangle(self.bounds())

    def get_first_route_segment(self) -> location.GeoRouteSegment:
        return location.GeoRouteSegment(self.firstRouteSegment())

    def get_path(self) -> list[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(i) for i in self.path()]
