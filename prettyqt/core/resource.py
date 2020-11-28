# -*- coding: utf-8 -*-

from typing import Iterator

import pathlib

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


COMPRESSION = bidict(
    none=QtCore.QResource.NoCompression,
    zlib=QtCore.QResource.ZlibCompression,
    zstd=QtCore.QResource.ZstdCompression,
)


class Resource(QtCore.QResource):
    def __repr__(self):
        return f"Resource({self.absoluteFilePath()!r}, {self.get_locale()!r})"

    def __bytes__(self):
        return bytes(self.uncompressedData())

    def __bool__(self):
        return self.isValid()

    def __iter__(self) -> Iterator[str]:
        return iter(self.children())

    def get_compression_algorithm(self) -> str:
        return COMPRESSION.inv[self.compressionAlgorithm()]

    def get_absolute_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.absoluteFilePath())

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_last_modified(self) -> core.DateTime:
        return core.DateTime(self.lastModified())
