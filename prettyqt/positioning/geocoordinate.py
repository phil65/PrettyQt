from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt.utils import bidict


QGeoCoordinate = QtPositioning.QGeoCoordinate

COORDINATE_FORMATS = bidict(
    default=QGeoCoordinate.Degrees,
    with_hemisphere=QGeoCoordinate.DegreesWithHemisphere,
    min=QGeoCoordinate.DegreesMinutes,
    min_with_hemisphere=QGeoCoordinate.DegreesMinutesWithHemisphere,
    min_sec=QGeoCoordinate.DegreesMinutesSeconds,
    min_sec_with_hemisphere=QGeoCoordinate.DegreesMinutesSecondsWithHemisphere,
)

COORDINATE_TYPES = bidict(
    invalid=QtPositioning.QGeoCoordinate.InvalidCoordinate,
    two_d=QtPositioning.QGeoCoordinate.Coordinate2D,
    three_d=QtPositioning.QGeoCoordinate.Coordinate3D,
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
