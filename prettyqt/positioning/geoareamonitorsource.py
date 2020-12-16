from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt import core
from prettyqt.utils import bidict


QtPositioning.QGeoAreaMonitorSource.__bases__ = (core.Object,)


ERRORS = bidict(
    access_error=QtPositioning.QGeoAreaMonitorSource.AccessError,
    insufficient_pos_info=QtPositioning.QGeoAreaMonitorSource.InsufficientPositionInfo,
    none=QtPositioning.QGeoAreaMonitorSource.NoError,
    unknown_source=QtPositioning.QGeoAreaMonitorSource.UnknownSourceError,
)

AREA_MONITOR_FEATURES = bidict(
    persistent_area=QtPositioning.QGeoAreaMonitorSource.PersistentAreaMonitorFeature,
    any_area=QtPositioning.QGeoAreaMonitorSource.AnyAreaMonitorFeature,
)


class GeoAreaMonitorSource(QtPositioning.QGeoAreaMonitorSource):
    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return f"{type(self).__name__}({self.name()!r})"

    def get_error(self) -> str:
        """Return error type.

        possible values: "access_error" "insufficient_pos_info", "none", "unkown_source"

        Returns:
            error type
        """
        return ERRORS.inverse[self.error()]


if __name__ == "__main__":
    coord = GeoAreaMonitorSource()
    print(str(coord))
    print(repr(coord))
