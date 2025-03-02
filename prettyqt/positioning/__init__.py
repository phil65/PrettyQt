"""Provides access to position, satellite info and area monitoring classes."""

from __future__ import annotations

from prettyqt.qt.QtPositioning import *  # noqa: F403

from .geoaddress import GeoAddress
from .geocoordinate import GeoCoordinate
from .geopositioninfo import GeoPositionInfo
from .geoshape import GeoShape, GeoShapeMixin
from .georectangle import GeoRectangle
from .geocircle import GeoCircle
from .geopath import GeoPath
from .geopolygon import GeoPolygon
from .geolocation import GeoLocation
from .geosatelliteinfo import GeoSatelliteInfo
from .geopositioninfosource import GeoPositionInfoSource, GeoPositionInfoSourceMixin
from .geosatelliteinfosource import GeoSatelliteInfoSource
from .nmeapositioninginfosource import NmeaPositionInfoSource
from .geoareamonitorinfo import GeoAreaMonitorInfo
from .geoareamonitorsource import GeoAreaMonitorSource
from prettyqt.qt import QtPositioning

QT_MODULE = QtPositioning

__all__ = [
    "GeoAddress",
    "GeoAreaMonitorInfo",
    "GeoAreaMonitorSource",
    "GeoCircle",
    "GeoCoordinate",
    "GeoLocation",
    "GeoPath",
    "GeoPolygon",
    "GeoPositionInfo",
    "GeoPositionInfoSource",
    "GeoPositionInfoSourceMixin",
    "GeoRectangle",
    "GeoSatelliteInfo",
    "GeoSatelliteInfoSource",
    "GeoShape",
    "GeoShapeMixin",
    "NmeaPositionInfoSource",
]
