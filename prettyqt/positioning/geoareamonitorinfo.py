from __future__ import annotations

from prettyqt import core, positioning
from prettyqt.qt import QtPositioning


class GeoAreaMonitorInfo(QtPositioning.QGeoAreaMonitorInfo):
    def __str__(self):
        return self.name()

    def __repr__(self):
        return f"{type(self).__name__}({self.name()!r})"

    def get_area(self) -> positioning.GeoShape:
        area = self.area()
        match area:
            case QtPositioning.QGeoCircle():
                return positioning.GeoCircle(area)
            case QtPositioning.QGeoRectangle():
                return positioning.GeoRectangle(area)
            case QtPositioning.QGeoPath():
                return positioning.GeoPath(area)
            case QtPositioning.QGeoPolygon():
                return positioning.GeoPolygon(area)
            case QtPositioning.QGeoShape():
                return positioning.GeoShape(area)
            case _:
                raise RuntimeError()

    def get_expiration(self) -> core.DateTime:
        return core.DateTime(self.expiration())


if __name__ == "__main__":
    info = GeoAreaMonitorInfo("test")
    print(str(info))
    print(repr(info))
