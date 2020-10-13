# -*- coding: utf-8 -*-

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning


from prettyqt import positioning

QtPositioning.QGeoCircle.__bases__ = (positioning.GeoShape,)


class GeoCircle(QtPositioning.QGeoCircle):
    def __repr__(self):
        return f"GeoCircle({self.get_center()!r}, {self.radius()})"

    def get_center(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.center())


if __name__ == "__main__":
    coord = positioning.GeoCoordinate(1, 1)
    circle = GeoCircle(coord, 0.5)
    print(str(circle))
    print(repr(circle))
