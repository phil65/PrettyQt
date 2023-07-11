from __future__ import annotations

import pathlib

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


StandardLocationStr = Literal[
    "desktop",
    "documents",
    "fonts",
    "applications",
    "music",
    "movies",
    "pictures",
    "temp",
    "home",
    "cache",
    "generic_cache",
    "generic_data",
    "runtime",
    "config",
    "download",
    "generic_config",
    "app_data",
    "app_local_data",
    "app_config",
]

STANDARD_LOCATION: bidict[StandardLocationStr, QtCore.QStandardPaths.StandardLocation] = (
    bidict(
        desktop=QtCore.QStandardPaths.StandardLocation.DesktopLocation,
        documents=QtCore.QStandardPaths.StandardLocation.DocumentsLocation,
        fonts=QtCore.QStandardPaths.StandardLocation.FontsLocation,
        applications=QtCore.QStandardPaths.StandardLocation.ApplicationsLocation,
        music=QtCore.QStandardPaths.StandardLocation.MusicLocation,
        movies=QtCore.QStandardPaths.StandardLocation.MoviesLocation,
        pictures=QtCore.QStandardPaths.StandardLocation.PicturesLocation,
        temp=QtCore.QStandardPaths.StandardLocation.TempLocation,
        home=QtCore.QStandardPaths.StandardLocation.HomeLocation,
        cache=QtCore.QStandardPaths.StandardLocation.CacheLocation,
        generic_cache=QtCore.QStandardPaths.StandardLocation.GenericCacheLocation,
        generic_data=QtCore.QStandardPaths.StandardLocation.GenericDataLocation,
        runtime=QtCore.QStandardPaths.StandardLocation.RuntimeLocation,
        config=QtCore.QStandardPaths.StandardLocation.ConfigLocation,
        download=QtCore.QStandardPaths.StandardLocation.DownloadLocation,
        generic_config=QtCore.QStandardPaths.StandardLocation.GenericConfigLocation,
        app_data=QtCore.QStandardPaths.StandardLocation.AppDataLocation,
        app_local_data=QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation,
        app_config=QtCore.QStandardPaths.StandardLocation.AppConfigLocation,
    )
)


class StandardPaths(QtCore.QStandardPaths):
    """Methods for accessing standard paths."""

    @classmethod
    def get_display_name(cls, location: StandardLocationStr) -> str:
        return cls.displayName(STANDARD_LOCATION[location])

    @classmethod
    def get_writable_location(cls, location: StandardLocationStr) -> pathlib.Path | None:
        path = cls.writableLocation(STANDARD_LOCATION[location])
        return pathlib.Path(path) if path else None

    @classmethod
    def get_standard_locations(cls, location: StandardLocationStr) -> list[pathlib.Path]:
        paths = cls.standardLocations(STANDARD_LOCATION[location])
        return [pathlib.Path(p) for p in paths]
