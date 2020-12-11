from qtpy import QtLocation

from prettyqt import location


QtLocation.QGeoRouteLeg.__bases__ = (location.GeoRoute,)


class GeoRouteLeg(QtLocation.QGeoRouteLeg):
    pass
