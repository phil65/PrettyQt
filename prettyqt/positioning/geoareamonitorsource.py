from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPositioning
from prettyqt.utils import bidict, get_repr


mod = QtPositioning.QGeoAreaMonitorSource

ErrorStr = Literal["access_error", "insufficient_pos_info", "none", "unknown_source"]

ERRORS: bidict[ErrorStr, mod.Error] = bidict(
    access_error=mod.Error.AccessError,
    insufficient_pos_info=mod.Error.InsufficientPositionInfo,
    none=mod.Error.NoError,
    unknown_source=mod.Error.UnknownSourceError,
)

AreaMonitorFeatureStr = Literal["persistent_area", "any_area"]

AREA_MONITOR_FEATURES: bidict[AreaMonitorFeatureStr, mod.AreaMonitorFeature] = bidict(
    persistent_area=mod.AreaMonitorFeature.PersistentAreaMonitorFeature,
    any_area=mod.AreaMonitorFeature.AnyAreaMonitorFeature,
)


class GeoAreaMonitorSource(core.ObjectMixin, QtPositioning.QGeoAreaMonitorSource):
    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return get_repr(self, self.sourceName())

    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERRORS.inverse[self.error()]


if __name__ == "__main__":
    obj = core.Object()
    coord = GeoAreaMonitorSource(obj)
    print(coord)
    print(repr(coord))
