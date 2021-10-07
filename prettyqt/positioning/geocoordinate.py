from __future__ import annotations

from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


mod = QtPositioning.QGeoCoordinate

COORDINATE_FORMATS = bidict(
    default=mod.CoordinateFormat.Degrees,
    with_hemisphere=mod.CoordinateFormat.DegreesWithHemisphere,
    min=mod.CoordinateFormat.DegreesMinutes,
    min_with_hemisphere=mod.CoordinateFormat.DegreesMinutesWithHemisphere,
    min_sec=mod.CoordinateFormat.DegreesMinutesSeconds,
    min_sec_with_hemisphere=mod.CoordinateFormat.DegreesMinutesSecondsWithHemisphere,
)

COORDINATE_TYPES = bidict(
    invalid=mod.CoordinateType.InvalidCoordinate,
    two_d=mod.CoordinateType.Coordinate2D,
    three_d=mod.CoordinateType.Coordinate3D,
)


class GeoCoordinate(QtPositioning.QGeoCoordinate):
    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"{type(self).__name__}({self.latitude()}, {self.longitude()})"

    def __bool__(self):
        return self.isValid()

    def get_type(self) -> str:
        return COORDINATE_TYPES.inverse[self.type()]


if __name__ == "__main__":
    coord = GeoCoordinate(11, 11)
    print(str(coord))
    print(repr(coord))
