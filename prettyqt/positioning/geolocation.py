from __future__ import annotations

from prettyqt import positioning
from prettyqt.qt import QtPositioning


class GeoLocation(QtPositioning.QGeoLocation):
    def get_address(self) -> positioning.GeoAddress:
        return positioning.GeoAddress(self.address())

    def get_coordinate(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinate())

    def get_bounding_box(self) -> positioning.GeoRectangle:
        return positioning.GeoRectangle(self.boundingBox())
