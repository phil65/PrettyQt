from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt import core, positioning
from prettyqt.utils import bidict


ATTRIBUTE = bidict(
    direction=QtPositioning.QGeoPositionInfo.Direction,
    ground_speed=QtPositioning.QGeoPositionInfo.GroundSpeed,
    vertical_speed=QtPositioning.QGeoPositionInfo.VerticalSpeed,
    magnetic_variation=QtPositioning.QGeoPositionInfo.MagneticVariation,
    horizontal_accuracy=QtPositioning.QGeoPositionInfo.HorizontalAccuracy,
    vertical_accuracy=QtPositioning.QGeoPositionInfo.VerticalAccuracy,
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
