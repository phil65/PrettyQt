from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict


QtPositioning.QGeoAreaMonitorSource.__bases__ = (core.Object,)


mod = QtPositioning.QGeoAreaMonitorSource

ERRORS = bidict(
    access_error=mod.Error.AccessError,
    insufficient_pos_info=mod.Error.InsufficientPositionInfo,
    none=mod.Error.NoError,
    unknown_source=mod.Error.UnknownSourceError,
)

ErrorStr = Literal["access_error", "insufficient_pos_info", "none", "unknown_source"]

AREA_MONITOR_FEATURES = bidict(
    persistent_area=mod.AreaMonitorFeature.PersistentAreaMonitorFeature,
    any_area=mod.AreaMonitorFeature.AnyAreaMonitorFeature,
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
