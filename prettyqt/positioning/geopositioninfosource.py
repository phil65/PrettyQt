# -*- coding: utf-8 -*-

from typing import List

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError, helpers

QGeoPositionInfoSource = QtPositioning.QGeoPositionInfoSource

POSITIONING_METHODS = bidict(
    none=QGeoPositionInfoSource.NoPositioningMethods,
    satellite=QGeoPositionInfoSource.SatellitePositioningMethods,
    non_satellite=QGeoPositionInfoSource.NonSatellitePositioningMethods,
    all=QGeoPositionInfoSource.AllPositioningMethods,
)

ERRORS = bidict(
    access_error=QtPositioning.QGeoPositionInfoSource.AccessError,
    closed_error=QtPositioning.QGeoPositionInfoSource.ClosedError,
    none=QtPositioning.QGeoPositionInfoSource.NoError,
    unknown_source=QtPositioning.QGeoPositionInfoSource.UnknownSourceError,
)

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
        return "GeoPositionInfoSource()"

    def get_error(self) -> str:
        """Return error type.

        possible values are "access_error" "closed_error", "none", "unkown_source"

        Returns:
            error type
        """
        return ERRORS.inv[self.error()]

    def set_preferred_positioning_methods(self, *methods: str):
        """Set preferred positioning methods.

        valid values are "none", "satellite", "non_satellite", "all"

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

    def get_preferred_positioning_methods(self) -> List[str]:
        """Return list of preferred positioning methods.

        possible included values are "none", "satellite", "non_satellite", "all"

        Returns:
            list of preferred positioning methods
        """
        return [
            k
            for k, v in POSITIONING_METHODS.items()
            if v & self.preferredPositioningMethods()
        ]

    def get_supported_positioning_methods(self) -> List[str]:
        """Return list of supported positioning methods.

        possible included values are "none", "satellite", "non_satellite", "all"

        Returns:
            list of supported positioning methods
        """
        return [
            k
            for k, v in POSITIONING_METHODS.items()
            if v & self.supportedPositioningMethods()
        ]
