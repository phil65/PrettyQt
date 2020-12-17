from typing import List, Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict, helpers


QGeoPositionInfoSource = QtPositioning.QGeoPositionInfoSource

POSITIONING_METHODS = bidict(
    none=QGeoPositionInfoSource.NoPositioningMethods,
    satellite=QGeoPositionInfoSource.SatellitePositioningMethods,
    non_satellite=QGeoPositionInfoSource.NonSatellitePositioningMethods,
    all=QGeoPositionInfoSource.AllPositioningMethods,
)

PositioningMethodStr = Literal["none", "satellite", "non_satellite", "all"]

ERRORS = bidict(
    access_error=QtPositioning.QGeoPositionInfoSource.AccessError,
    closed_error=QtPositioning.QGeoPositionInfoSource.ClosedError,
    none=QtPositioning.QGeoPositionInfoSource.NoError,
    unknown_source=QtPositioning.QGeoPositionInfoSource.UnknownSourceError,
)

ErrorStr = Literal["access_error", "closed_error", "none", "unknown_source"]

QtPositioning.QGeoPositionInfoSource.__bases__ = (core.Object,)


class GeoPositionInfoSource(QtPositioning.QGeoPositionInfoSource):
    def serialize_fields(self):
        return dict(
            minimum_update_interval=self.minimumUpdateInterval(),
            source_name=self.sourceName(),
            update_interval=self.updateInterval(),
        )

    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return f"{type(self).__name__}()"

    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERRORS.inverse[self.error()]

    def set_preferred_positioning_methods(self, *methods: PositioningMethodStr):
        """Set preferred positioning methods.

        Args:
            methods: positioning methods to use

        Raises:
            InvalidParamError: invalid positioning methods
        """
        for item in methods:
            if item not in POSITIONING_METHODS:
                raise InvalidParamError(item, POSITIONING_METHODS)
        flags = helpers.merge_flags(methods, POSITIONING_METHODS)
        self.setPreferredPositioningMethods(flags)

    def get_preferred_positioning_methods(self) -> List[PositioningMethodStr]:
        """Return list of preferred positioning methods.

        Returns:
            list of preferred positioning methods
        """
        return [
            k
            for k, v in POSITIONING_METHODS.items()
            if v & self.preferredPositioningMethods()
        ]

    def get_supported_positioning_methods(self) -> List[PositioningMethodStr]:
        """Return list of supported positioning methods.

        Returns:
            list of supported positioning methods
        """
        return [
            k
            for k, v in POSITIONING_METHODS.items()
            if v & self.supportedPositioningMethods()
        ]
