from __future__ import annotations

from prettyqt import positioning
from prettyqt.qt import QtPositioning


class GeoRectangle(positioning.GeoShapeMixin, QtPositioning.QGeoRectangle):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.get_top_left()!r}, {self.get_bottom_right()!r})"
        )

    def get_top_left(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.topLeft())

    def get_bottom_right(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.bottomRight())


if __name__ == "__main__":
    coord1 = positioning.GeoCoordinate(1, 1)
    coord2 = positioning.GeoCoordinate(11, 11)
    rect = GeoRectangle(coord1, coord2)
    print(rect)
    print(repr(rect))
