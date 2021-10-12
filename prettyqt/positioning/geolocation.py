from __future__ import annotations

from prettyqt import core, positioning
from prettyqt.qt import QtPositioning


class GeoLocation(QtPositioning.QGeoLocation):
    def get_address(self) -> positioning.GeoAddress:
        return positioning.GeoAddress(self.address())

    def get_coordinate(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinate())

    def get_bounding_shape(self) -> positioning.GeoShape:
        if core.VersionNumber.get_qt_version() < (6, 0, 0):
            return positioning.GeoRectangle(self.boundingBox())
        else:
            return positioning.GeoShape(self.boundingShape())


if __name__ == "__main__":
    location = GeoLocation()
