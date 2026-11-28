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


CoordinateTypeStr = Literal["invalid", "2d", "3d"]

COORDINATE_TYPE: bidict[CoordinateTypeStr, mod.CoordinateType] = bidict({
    "invalid": mod.CoordinateType.InvalidCoordinate,
    "2d": mod.CoordinateType.Coordinate2D,
    "3d": mod.CoordinateType.Coordinate3D,
})


class GeoCoordinate(QtPositioning.QGeoCoordinate):
    def __str__(self):
        return self.toString()

    def __format__(self, format_spec: CoordinateFormatStr | Literal[""]):
        if not format_spec:
            return self.toString()
        return self.toString(COORDINATE_FORMAT[format_spec])

    def __repr__(self):
        return get_repr(self, self.latitude(), self.longitude())

    def __bool__(self):
        return self.isValid()

    def get_type(self) -> CoordinateTypeStr:
        return COORDINATE_TYPE.inverse[self.type()]


if __name__ == "__main__":
    coord = GeoCoordinate(11, 11)
    print(coord)
    print(repr(coord))
