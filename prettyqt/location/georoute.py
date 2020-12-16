from typing import List

from qtpy import QtLocation

from prettyqt import location, positioning


class GeoRoute(QtLocation.QGeoRoute):
    def __setitem__(self, index: str, val):
        attrs = self.extendedAttributes()
        attrs[index] = val
        self.setExtendedAttributes(attrs)

    def __getitem__(self, index: str):
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

    def get_path(self) -> List[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(i) for i in self.path()]
