from __future__ import annotations

from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


SHAPE_TYPES = bidict(
    unknown=QtPositioning.QGeoShape.UnknownType,
    rectangle=QtPositioning.QGeoShape.RectangleType,
    circle=QtPositioning.QGeoShape.CircleType,
    path=QtPositioning.QGeoShape.PathType,
    polygon=QtPositioning.QGeoShape.PolygonType,
)


class GeoShape(QtPositioning.QGeoShape):
    def __contains__(self, other: QtPositioning.QGeoCoordinate):
        return self.contains(other)

    def __str__(self):
        return self.toString()[1:]

    def get_type(self) -> str:
        return SHAPE_TYPES.inverse[self.type()]
