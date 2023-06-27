from __future__ import annotations

from collections.abc import Iterable
import os
import pathlib

from prettyqt import core
from prettyqt.utils import datatypes, get_repr


class FileSystemWatcher(core.ObjectMixin, core.QFileSystemWatcher):
    def __repr__(self):
        return get_repr(self, self.directories() + self.files())

    def get_directories(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.directories()]

    def get_files(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.files()]

    def get_paths(self) -> list[pathlib.Path]:
        return self.get_directories() + self.get_files()

    def add_path(self, path: datatypes.PathType) -> bool:
        return self.addPath(os.fspath(path))

    def add_paths(self, paths: Iterable[datatypes.PathType]):
        self.addPaths([os.fspath(p) for p in paths])
