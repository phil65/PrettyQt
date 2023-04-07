from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


class GeoRouteLeg(location.GeoRouteMixin, QtLocation.QGeoRouteLeg):  # type: ignore
    pass
