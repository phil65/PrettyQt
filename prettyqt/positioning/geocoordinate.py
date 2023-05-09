from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict, get_repr


mod = QtPositioning.QGeoCoordinate

COORDINATE_FORMAT = bidict(
    default=mod.CoordinateFormat.Degrees,
    with_hemisphere=mod.CoordinateFormat.DegreesWithHemisphere,
    min=mod.CoordinateFormat.DegreesMinutes,
    min_with_hemisphere=mod.CoordinateFormat.DegreesMinutesWithHemisphere,
    min_sec=mod.CoordinateFormat.DegreesMinutesSeconds,
    min_sec_with_hemisphere=mod.CoordinateFormat.DegreesMinutesSecondsWithHemisphere,
)

CoordinateFormatStr = Literal[
    "default",
    "with_hemisphere",
    "min",
    "min_with_hemisphere",
    "min_sec",
    "min_sec_with_hemisphere",
]


COORDINATE_TYPE = bidict(
    {
        "invalid": mod.CoordinateType.InvalidCoordinate,
        "2d": mod.CoordinateType.Coordinate2D,
        "3d": mod.CoordinateType.Coordinate3D,
    }
)

CoordinateTypeStr = Literal["invalid", "2d", "3d"]


class GeoCoordinate(QtPositioning.QGeoCoordinate):
    def __str__(self):
        return self.toString()

    def __format__(self, format_spec: CoordinateFormatStr):
        return self.toString(COORDINATE_FORMAT[format_spec])

    def __repr__(self):
        return get_repr(self, self.latitude(), self.longitude())

    def __bool__(self):
        return self.isValid()

    def get_type(self) -> str:
        return COORDINATE_TYPE.inverse[self.type()]


if __name__ == "__main__":
    coord = GeoCoordinate(11, 11)
    print(coord)
    print(repr(coord))
