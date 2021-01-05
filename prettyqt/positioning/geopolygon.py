from __future__ import annotations

from typing import List

from prettyqt import positioning
from prettyqt.qt import QtPositioning


QtPositioning.QGeoPolygon.__bases__ = (positioning.GeoShape,)


class GeoPolygon(QtPositioning.QGeoPolygon):
    def __len__(self):
        return self.size()

    def __repr__(self):
        # p = ", ".join([f"{p!r}" for p in self.get_path()])
        return f"{type(self).__name__}(<{len(self)} points>)"

    def __getitem__(self, index: int) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinateAt(index))

    def __setitem__(self, index: int, value: QtPositioning.QGeoCoordinate):
        self.replaceCoordinate(index, value)

    def __delitem__(self, index: int):
        self.removeCoordinate(index)

    def __add__(self, other: QtPositioning.QGeoCoordinate):
        self.addCoordinate(other)
        return self

    def get_path(self) -> List[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(p) for p in self.path()]


if __name__ == "__main__":
    poly = GeoPolygon()
    coord = positioning.GeoCoordinate(11, 11)
    poly += coord
    poly.addCoordinate(coord)
    print(len(poly))
    print(str(poly))
