from __future__ import annotations

from typing import Optional, Tuple, Union

from prettyqt import positioning
from prettyqt.qt import QtPositioning


QtPositioning.QGeoCircle.__bases__ = (positioning.GeoShape,)


class GeoCircle(QtPositioning.QGeoCircle):
    def __init__(
        self,
        center_or_other: Optional[
            Union[
                QtPositioning.QGeoShape, QtPositioning.QGeoCoordinate, Tuple[float, float]
            ]
        ] = None,
        radius: Optional[float] = None,
    ):
        if center_or_other is None:
            super().__init__()
        else:
            if radius is None:
                radius = -1
            if isinstance(center_or_other, tuple):
                center_or_other = QtPositioning.QGeoCoordinate(*center_or_other)
            super().__init__(center_or_other, radius)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_center()!r}, {self.radius()})"

    def get_center(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.center())


if __name__ == "__main__":
    coord = (1, 1)
    circle = GeoCircle(coord)
    print(str(circle))
    print(repr(circle))
