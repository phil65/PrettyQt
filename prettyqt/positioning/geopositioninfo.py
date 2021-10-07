from __future__ import annotations

from typing import Literal

from prettyqt import core, positioning
from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


ATTRIBUTE = bidict(
    direction=QtPositioning.QGeoPositionInfo.Attribute.Direction,
    ground_speed=QtPositioning.QGeoPositionInfo.Attribute.GroundSpeed,
    vertical_speed=QtPositioning.QGeoPositionInfo.Attribute.VerticalSpeed,
    magnetic_variation=QtPositioning.QGeoPositionInfo.Attribute.MagneticVariation,
    horizontal_accuracy=QtPositioning.QGeoPositionInfo.Attribute.HorizontalAccuracy,
    vertical_accuracy=QtPositioning.QGeoPositionInfo.Attribute.VerticalAccuracy,
)

AttributeStr = Literal[
    "direction",
    "ground_speed",
    "vertical_speed",
    "magnetic_variation",
    "horizontal_accuracy",
    "vertical_accuracy",
]


class GeoPositionInfo(QtPositioning.QGeoPositionInfo):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_coordinate()}, {self.get_timestamp()})"

    def __contains__(self, index: AttributeStr):
        return self.hasAttribute(ATTRIBUTE[index])

    def __getitem__(self, index: AttributeStr) -> float:
        return self.attribute(ATTRIBUTE[index])

    def __setitem__(self, index: AttributeStr, value: float):
        self.setAttribute(ATTRIBUTE[index], value)

    def __delitem__(self, index: AttributeStr):
        return self.removeAttribute(ATTRIBUTE[index])

    def __bool__(self):
        return self.isValid()

    def get_coordinate(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinate())

    def get_timestamp(self) -> core.DateTime:
        return core.DateTime(self.timestamp())
