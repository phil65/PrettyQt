from qtpy import QtLocation

from prettyqt import location


# not available in PySide2

QtLocation.QGeoRouteLeg.__bases__ = (location.GeoRoute,)  # type: ignore


class GeoRouteLeg(QtLocation.QGeoRouteLeg):  # type: ignore
    pass
