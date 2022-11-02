from __future__ import annotations

from collections.abc import Iterator
import os
import pathlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, types


COMPRESSION = bidict(
    none=QtCore.QResource.Compression.NoCompression,
    zlib=QtCore.QResource.Compression.ZlibCompression,
    zstd=QtCore.QResource.Compression.ZstdCompression,
)

CompressionStr = Literal["none", "zlib", "zstd"]


class Resource(QtCore.QResource):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.absoluteFilePath()!r}, "
            f"{self.get_locale()!r})"
        )

    def __reduce__(self):
        return type(self), (self.absoluteFilePath(), self.get_locale())

    def __bytes__(self):
        return bytes(self.uncompressedData())

    def __bool__(self):
        return self.isValid()

    def __iter__(self) -> Iterator[str]:
        return iter(self.children())

    def get_compression_algorithm(self) -> CompressionStr:
        return COMPRESSION.inverse[self.compressionAlgorithm()]

    def get_absolute_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.absoluteFilePath())

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_last_modified(self) -> core.DateTime:
        return core.DateTime(self.lastModified())

    def set_file_name(self, path: types.PathType):
        self.setFileName(os.fspath(path))

    def get_file_name(self) -> pathlib.Path:
        return pathlib.Path(self.fileName())

    @classmethod
    def register_resource(cls, path: types.PathType, root: str = ""):
        cls.registerResource(os.fspath(path), root)
