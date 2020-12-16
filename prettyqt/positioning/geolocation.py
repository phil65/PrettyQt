from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt import positioning


class GeoLocation(QtPositioning.QGeoLocation):
    def get_address(self) -> positioning.GeoAddress:
        return positioning.GeoAddress(self.address())

    def get_coordinate(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.coordinate())

    def get_bounding_box(self) -> positioning.GeoRectangle:
        return positioning.GeoRectangle(self.boundingBox())
