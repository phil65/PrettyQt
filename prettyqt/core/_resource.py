from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.utils import bidict, get_repr


if TYPE_CHECKING:
    from collections.abc import Iterator

    from prettyqt.utils import datatypes


CompressionStr = Literal["none", "zlib", "zstd"]

COMPRESSION: bidict[CompressionStr, core.QResource.Compression] = bidict(
    none=core.QResource.Compression.NoCompression,
    zlib=core.QResource.Compression.ZlibCompression,
    zstd=core.QResource.Compression.ZstdCompression,
)


class Resource(core.QResource):
    """Interface for reading directly from resources."""

    def __repr__(self):
        return get_repr(self, self.absoluteFilePath(), self.get_locale())

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

    def set_file_name(self, path: datatypes.PathType):
        self.setFileName(os.fspath(path))

    def get_file_name(self) -> pathlib.Path:
        return pathlib.Path(self.fileName())

    @classmethod
    def register_resource(cls, path: datatypes.PathType, root: str = ""):
        cls.registerResource(os.fspath(path), root)
