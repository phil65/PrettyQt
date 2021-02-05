from __future__ import annotations

import os
import pathlib

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QFileSystemWatcher.__bases__ = (core.Object,)


class FileSystemWatcher(QtCore.QFileSystemWatcher):
    def __repr__(self):
        paths = [str(p) for p in self.get_paths()]
        return f"{type(self).__name__}({paths})"

    def get_directories(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.directories()]

    def get_files(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.files()]

    def get_paths(self) -> list[pathlib.Path]:
        return self.get_directories() + self.get_files()

    def add_path(self, path: str | os.PathLike) -> bool:
        return self.addPath(os.fspath(path))

    def add_paths(self, paths: list[str | os.PathLike]):
        self.addPaths([os.fspath(p) for p in paths])
