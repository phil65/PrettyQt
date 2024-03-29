from __future__ import annotations

from prettyqt import positioning
from prettyqt.qt import QtPositioning
from prettyqt.utils import get_repr


class GeoCircle(positioning.GeoShapeMixin, QtPositioning.QGeoCircle):
    def __init__(
        self,
        center_or_other: None
        | (
            QtPositioning.QGeoShape | QtPositioning.QGeoCoordinate | tuple[float, float]
        ) = None,
        radius: float | None = None,
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
        return get_repr(self, self.get_center(), self.radius())

    def get_center(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.center())


if __name__ == "__main__":
    coord = (1, 1)
    circle = GeoCircle(coord)
    print(circle)
    print(repr(circle))
