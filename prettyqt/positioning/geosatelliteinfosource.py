# -*- coding: utf-8 -*-

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning


from prettyqt import core
from prettyqt.utils import bidict

ERRORS = bidict(
    access_error=QtPositioning.QGeoSatelliteInfoSource.AccessError,
    closed_error=QtPositioning.QGeoSatelliteInfoSource.ClosedError,
    none=QtPositioning.QGeoSatelliteInfoSource.NoError,
    unknown_source=QtPositioning.QGeoSatelliteInfoSource.UnknownSourceError,
)

QtPositioning.QGeoSatelliteInfoSource.__bases__ = (core.Object,)


class GeoSatelliteInfoSource(QtPositioning.QGeoSatelliteInfoSource):
    def serialize_fields(self):
        return dict(
            minimum_update_interval=self.minimumUpdateInterval(),
            update_interval=self.updateInterval(),
        )

    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return "GeoSatelliteInfoSource()"

    def get_error(self) -> str:
        """Return error type.

        possible values are "access_error" "closed_error", "none", "unkown_source"

        Returns:
            error type
        """
        return ERRORS.inv[self.error()]
