from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt.utils import InvalidParamError, bidict


SATELLITE_SYSTEMS = bidict(
    undefined=QtPositioning.QGeoSatelliteInfo.Undefined,
    gps=QtPositioning.QGeoSatelliteInfo.GPS,
    glonass=QtPositioning.QGeoSatelliteInfo.GLONASS,
)

SatelliteSystemStr = Literal["undefined", "gps", "glonass"]

ATTRIBUTE = bidict(
    elevation=QtPositioning.QGeoSatelliteInfo.Elevation,
    azimuth=QtPositioning.QGeoSatelliteInfo.Azimuth,
)

AttributeStr = Literal["elevation", "azimuth"]


class GeoSatelliteInfo(QtPositioning.QGeoSatelliteInfo):
    def __getitem__(self, index: AttributeStr):
        return self.attribute(ATTRIBUTE[index])

    def __setitem__(self, index: AttributeStr, value: float):
        self.setAttribute(ATTRIBUTE[index], value)

    def __delitem__(self, index: AttributeStr):
        self.removeAttribute(ATTRIBUTE[index])

    def __contains__(self, value: AttributeStr):
        return self.hasAttribute(ATTRIBUTE[value])

    def __int__(self):
        return self.satelliteIdentifier()

    def set_satellite_system(self, system: SatelliteSystemStr):
        """Set satellite system.

        Args:
            system: satellite system to use

        Raises:
            InvalidParamError: invalid system
        """
        if system not in SATELLITE_SYSTEMS:
            raise InvalidParamError(system, SATELLITE_SYSTEMS)
        self.setSatelliteSystem(SATELLITE_SYSTEMS[system])

    def get_satellite_system(self) -> SatelliteSystemStr:
        """Return satellite system.

        Returns:
            satellite system
        """
        return SATELLITE_SYSTEMS.inverse[self.satelliteSystem()]


if __name__ == "__main__":
    coord = GeoSatelliteInfo()
