# -*- coding: utf-8 -*-

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning


from prettyqt.utils import bidict, InvalidParamError

SATELLITE_SYSTEMS = bidict(
    undefined=QtPositioning.QGeoSatelliteInfo.Undefined,
    gps=QtPositioning.QGeoSatelliteInfo.GPS,
    glonass=QtPositioning.QGeoSatelliteInfo.GLONASS,
)

ATTRIBUTES = bidict(
    elevation=QtPositioning.QGeoSatelliteInfo.Elevation,
    azimuth=QtPositioning.QGeoSatelliteInfo.Azimuth,
)


class GeoSatelliteInfo(QtPositioning.QGeoSatelliteInfo):
    def __getitem__(self, index: str):
        return self.attribute(ATTRIBUTES[index])

    def __setitem__(self, index: str, value: float):
        self.setAttribute(ATTRIBUTES[index], value)

    def __delitem__(self, index: str):
        self.removeAttribute(ATTRIBUTES[index])

    def __contains__(self, value: str):
        return self.hasAttribute(ATTRIBUTES[value])

    def __int__(self):
        return self.satelliteIdentifier()

    def set_satellite_system(self, system: str):
        """Set satellite system.

        valid values are: "undefined", "gps", "glonass"

        Args:
            system: satellite system to use

        Raises:
            InvalidParamError: invalid system
        """
        if system not in SATELLITE_SYSTEMS:
            raise InvalidParamError(system, SATELLITE_SYSTEMS)
        self.setSatelliteSystem(SATELLITE_SYSTEMS[system])

    def get_satellite_system(self) -> bool:
        """Return satellite system.

        possible values are "undefined", "gps", "glonass"

        Returns:
            satellite system
        """
        return SATELLITE_SYSTEMS.inv[self.satelliteSystem()]


if __name__ == "__main__":
    coord = GeoSatelliteInfo()
