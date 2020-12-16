import pathlib
from typing import List, Literal, Optional

from qtpy import QtCore

from prettyqt.utils import bidict


STANDARD_LOCATION = bidict(
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


class StandardPaths(QtCore.QStandardPaths):
    def __class_getitem__(cls, name: StandardLocationStr) -> List[pathlib.Path]:
        return cls.get_standard_locations(name)

    @classmethod
    def get_display_name(cls, location: StandardLocationStr) -> str:
        return cls.displayName(STANDARD_LOCATION[location])

    @classmethod
    def get_writable_location(
        cls, location: StandardLocationStr
    ) -> Optional[pathlib.Path]:
        path = cls.writableLocation(STANDARD_LOCATION[location])
        return pathlib.Path(path) if path else None

    @classmethod
    def get_standard_locations(cls, location: StandardLocationStr) -> List[pathlib.Path]:
        paths = cls.standardLocations(STANDARD_LOCATION[location])
        return [pathlib.Path(p) for p in paths]
