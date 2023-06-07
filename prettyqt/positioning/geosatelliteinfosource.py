from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict, get_repr


ERROR = bidict(
    access_error=QtPositioning.QGeoSatelliteInfoSource.Error.AccessError,
    closed_error=QtPositioning.QGeoSatelliteInfoSource.Error.ClosedError,
    none=QtPositioning.QGeoSatelliteInfoSource.Error.NoError,
    unknown_source=QtPositioning.QGeoSatelliteInfoSource.Error.UnknownSourceError,
)

ErrorStr = Literal["access_error", "closed_error", "none", "unknown_source"]


class GeoSatelliteInfoSource(core.ObjectMixin, QtPositioning.QGeoSatelliteInfoSource):
    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return get_repr(self)

    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERROR.inverse[self.error()]
