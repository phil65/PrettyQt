from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


QtPositioning.QGeoAreaMonitorSource.__bases__ = (core.Object,)


ERRORS = bidict(
    access_error=QtPositioning.QGeoAreaMonitorSource.AccessError,
    insufficient_pos_info=QtPositioning.QGeoAreaMonitorSource.InsufficientPositionInfo,
    none=QtPositioning.QGeoAreaMonitorSource.NoError,
    unknown_source=QtPositioning.QGeoAreaMonitorSource.UnknownSourceError,
)

ErrorStr = Literal["access_error", "insufficient_pos_info", "none", "unknown_source"]

AREA_MONITOR_FEATURES = bidict(
    persistent_area=QtPositioning.QGeoAreaMonitorSource.PersistentAreaMonitorFeature,
    any_area=QtPositioning.QGeoAreaMonitorSource.AnyAreaMonitorFeature,
)

AreaMonitorFeatureStr = Literal["persistent_area", "any_area"]


class GeoAreaMonitorSource(QtPositioning.QGeoAreaMonitorSource):
    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return f"{type(self).__name__}({self.name()!r})"

    def get_error(self) -> AreaMonitorFeatureStr:
        """Return error type.

        Returns:
            error type
        """
        return ERRORS.inverse[self.error()]


if __name__ == "__main__":
    obj = core.Object()
    coord = GeoAreaMonitorSource(obj)
    print(str(coord))
    print(repr(coord))
