from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import core, qt
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


mod = QtCore.QLibraryInfo.LibraryPath

LOCATION = bidict(
    prefix=mod.PrefixPath,
    documentation=mod.DocumentationPath,
    headers=mod.HeadersPath,
    libraries=mod.LibrariesPath,
    library_executables=mod.LibraryExecutablesPath,
    binaries=mod.BinariesPath,
    plugins=mod.PluginsPath,
    qml2_imports=mod.Qml2ImportsPath,
    arch_data=mod.ArchDataPath,
    data=mod.DataPath,
    translations=mod.TranslationsPath,
    examples=mod.ExamplesPath,
    tests=mod.TestsPath,
    settings=mod.SettingsPath,
)

LocationStr = Literal[
    "prefix",
    "documentation",
    "headers",
    "libraries",
    "library_executables",
    "binaries",
    "plugins",
    "qml2_imports",
    "arch_data",
    "data",
    "translations",
    "examples",
    "tests",
    "settings",
]


class LibraryInfo(QtCore.QLibraryInfo):
    def __class_getitem__(cls, name: LocationStr) -> pathlib.Path:
        return cls.get_location(name)

    @classmethod
    def get_location(cls, location: LocationStr) -> pathlib.Path:
        if location not in LOCATION:
            raise InvalidParamError(location, LOCATION)
        if qt.API.endswith("6"):
            path = cls.path(LOCATION[location])
        else:
            path = cls.location(LOCATION[location])
        return pathlib.Path(path)

    @classmethod
    def get_version(cls) -> core.VersionNumber:
        return core.VersionNumber(cls.version())


if __name__ == "__main__":
    path = LibraryInfo.get_location("prefix")
    print(path)
