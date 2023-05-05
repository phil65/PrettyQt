from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPositioning
from prettyqt.utils import InvalidParamError, bidict, get_repr


QGeoPositionInfoSource = QtPositioning.QGeoPositionInfoSource

POSITIONING_METHODS = bidict(
    none=QGeoPositionInfoSource.PositioningMethod.NoPositioningMethods,
    satellite=QGeoPositionInfoSource.PositioningMethod.SatellitePositioningMethods,
    non_satellite=QGeoPositionInfoSource.PositioningMethod.NonSatellitePositioningMethods,
    all=QGeoPositionInfoSource.PositioningMethod.AllPositioningMethods,
)

PositioningMethodStr = Literal["none", "satellite", "non_satellite", "all"]

ERRORS = bidict(
    access_error=QGeoPositionInfoSource.Error.AccessError,
    closed_error=QGeoPositionInfoSource.Error.ClosedError,
    none=QGeoPositionInfoSource.Error.NoError,
    unknown_source=QGeoPositionInfoSource.Error.UnknownSourceError,
)

ErrorStr = Literal["access_error", "closed_error", "none", "unknown_source"]


class GeoPositionInfoSourceMixin(core.ObjectMixin):
    def serialize_fields(self):
        return dict(
            minimum_update_interval=self.minimumUpdateInterval(),
            source_name=self.sourceName(),
            update_interval=self.updateInterval(),
        )

    def __str__(self):
        return self.sourceName()

    def __repr__(self):
        return get_repr(self)

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
        flags = POSITIONING_METHODS.merge_flags(methods)
        self.setPreferredPositioningMethods(flags)

    def get_preferred_positioning_methods(self) -> list[PositioningMethodStr]:
        """Return list of preferred positioning methods.

        Returns:
            list of preferred positioning methods
        """
        return POSITIONING_METHODS.get_list(self.preferredPositioningMethods())

    def get_supported_positioning_methods(self) -> list[PositioningMethodStr]:
        """Return list of supported positioning methods.

        Returns:
            list of supported positioning methods
        """
        return POSITIONING_METHODS.get_list(self.supportedPositioningMethods())


class GeoPositionInfoSource(
    GeoPositionInfoSourceMixin, QtPositioning.QGeoPositionInfoSource
):
    pass
