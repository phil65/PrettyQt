# -*- coding: utf-8 -*-

from typing import List, Optional
import pathlib

from qtpy import QtCore

from prettyqt.utils import bidict

STANDARD_LOCATIONS = bidict(
    desktop=QtCore.QStandardPaths.DesktopLocation,
    documents=QtCore.QStandardPaths.DocumentsLocation,
    fonts=QtCore.QStandardPaths.FontsLocation,
    applications=QtCore.QStandardPaths.ApplicationsLocation,
    music=QtCore.QStandardPaths.MusicLocation,
    movies=QtCore.QStandardPaths.MoviesLocation,
    pictures=QtCore.QStandardPaths.PicturesLocation,
    temp=QtCore.QStandardPaths.TempLocation,
    home=QtCore.QStandardPaths.HomeLocation,
    cache=QtCore.QStandardPaths.CacheLocation,
    generic_cache=QtCore.QStandardPaths.GenericCacheLocation,
    generic_data=QtCore.QStandardPaths.GenericDataLocation,
    runtime=QtCore.QStandardPaths.RuntimeLocation,
    config=QtCore.QStandardPaths.ConfigLocation,
    download=QtCore.QStandardPaths.DownloadLocation,
    generic_config=QtCore.QStandardPaths.GenericConfigLocation,
    app_data=QtCore.QStandardPaths.AppDataLocation,
    app_local_data=QtCore.QStandardPaths.AppLocalDataLocation,
    app_config=QtCore.QStandardPaths.AppConfigLocation,
)


class StandardPaths(QtCore.QStandardPaths):
    def __class_getitem__(cls, name: str) -> List[pathlib.Path]:
        return cls.get_standard_locations(name)

    @classmethod
    def get_display_name(cls, location: str) -> str:
        return cls.displayName(STANDARD_LOCATIONS[location])

    @classmethod
    def get_writable_location(cls, location: str) -> Optional[pathlib.Path]:
        path = cls.writableLocation(STANDARD_LOCATIONS[location])
        return pathlib.Path(path) if path else None

    @classmethod
    def get_standard_locations(cls, location: str) -> List[pathlib.Path]:
        paths = cls.standardLocations(STANDARD_LOCATIONS[location])
        return [pathlib.Path(p) for p in paths]
