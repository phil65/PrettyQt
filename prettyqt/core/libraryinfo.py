import pathlib
from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


LOCATION = bidict(
    prefix=QtCore.QLibraryInfo.PrefixPath,
    documentation=QtCore.QLibraryInfo.DocumentationPath,
    headers=QtCore.QLibraryInfo.HeadersPath,
    libraries=QtCore.QLibraryInfo.LibrariesPath,
    library_executables=QtCore.QLibraryInfo.LibraryExecutablesPath,
    binaries=QtCore.QLibraryInfo.BinariesPath,
    plugins=QtCore.QLibraryInfo.PluginsPath,
    imports=QtCore.QLibraryInfo.ImportsPath,
    qml2_imports=QtCore.QLibraryInfo.Qml2ImportsPath,
    arch_data=QtCore.QLibraryInfo.ArchDataPath,
    data=QtCore.QLibraryInfo.DataPath,
    translations=QtCore.QLibraryInfo.TranslationsPath,
    examples=QtCore.QLibraryInfo.ExamplesPath,
    tests=QtCore.QLibraryInfo.TestsPath,
    settings=QtCore.QLibraryInfo.SettingsPath,
)

LocationStr = Literal[
    "prefix",
    "documentation",
    "headers",
    "libraries",
    "library_executables",
    "binaries",
    "plugins",
    "imports",
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
        return pathlib.Path(cls.location(LOCATION[location]))

    @classmethod
    def get_version(cls) -> core.VersionNumber:
        return core.VersionNumber(cls.version())


if __name__ == "__main__":
    path = LibraryInfo.get_location("prefix")
    print(path)
