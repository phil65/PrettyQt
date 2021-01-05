from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


# not available in PySide2

QtLocation.QGeoRouteLeg.__bases__ = (location.GeoRoute,)  # type: ignore


class GeoRouteLeg(QtLocation.QGeoRouteLeg):  # type: ignore
    pass
