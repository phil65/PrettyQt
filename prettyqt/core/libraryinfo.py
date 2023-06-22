from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


mod = QtCore.QLibraryInfo.LibraryPath

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

LOCATION: bidict[LocationStr, mod] = bidict(
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


class LibraryInfo(QtCore.QLibraryInfo):
    @classmethod
    def get_location(cls, location: LocationStr) -> pathlib.Path:
        if location not in LOCATION:
            raise InvalidParamError(location, LOCATION)
        path = cls.path(LOCATION[location])
        return pathlib.Path(path)

    @classmethod
    def get_version(cls) -> core.VersionNumber:
        return core.VersionNumber(cls.version())


if __name__ == "__main__":
    path = LibraryInfo.get_location("prefix")
