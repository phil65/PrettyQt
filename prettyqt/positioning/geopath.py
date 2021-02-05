from __future__ import annotations

from prettyqt import positioning
from prettyqt.qt import QtPositioning


QtPositioning.QGeoPath.__bases__ = (positioning.GeoShape,)


class GeoPath(QtPositioning.QGeoPath):
    def __len__(self):
        return self.size()

    def __getitem__(self, index: int) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinateAt(index))

    def __setitem__(self, index: int, value: QtPositioning.QGeoCoordinate):
        self.replaceCoordinate(index, value)

    def __delitem__(self, index: int):
        self.removeCoordinate(index)

    def __add__(self, other: QtPositioning.QGeoCoordinate):
        self.addCoordinate(other)
        return self

    def __repr__(self):
        # p = ", ".join([f"{p!r}" for p in self.get_path()])
        return f"{type(self).__name__}(<{len(self)} points>)"

    def get_path(self) -> list[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(p) for p in self.path()]


if __name__ == "__main__":
    path = GeoPath()
    print(str(path))
