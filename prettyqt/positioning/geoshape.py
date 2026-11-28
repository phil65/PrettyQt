from typing import TYPE_CHECKING, Literal

from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


ShapeTypeStr = Literal["unknown", "rectangle", "circle", "path", "polygon"]

SHAPE_TYPES: bidict[ShapeTypeStr, QtPositioning.QGeoShape.ShapeType] = bidict(
    unknown=QtPositioning.QGeoShape.ShapeType.UnknownType,
    rectangle=QtPositioning.QGeoShape.ShapeType.RectangleType,
    circle=QtPositioning.QGeoShape.ShapeType.CircleType,
    path=QtPositioning.QGeoShape.ShapeType.PathType,
    polygon=QtPositioning.QGeoShape.ShapeType.PolygonType,
)


if TYPE_CHECKING:
    _GeoShapeBase = QtPositioning.QGeoShape
else:
    _GeoShapeBase = object


class GeoShapeMixin(_GeoShapeBase):
    def __contains__(self, other: QtPositioning.QGeoCoordinate):
        return self.contains(other)

    def __str__(self):
        return self.toString()[1:]

    def get_type(self) -> ShapeTypeStr:
        return SHAPE_TYPES.inverse[self.type()]


class GeoShape(GeoShapeMixin, QtPositioning.QGeoShape):
    pass
