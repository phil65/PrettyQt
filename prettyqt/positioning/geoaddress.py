from __future__ import annotations

from prettyqt.qt import QtPositioning


class GeoAddress(QtPositioning.QGeoAddress):
    def __str__(self):
        return self.text()
