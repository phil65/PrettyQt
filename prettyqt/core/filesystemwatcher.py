from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from collections.abc import Iterable

    from prettyqt.utils import datatypes


class FileSystemWatcher(core.ObjectMixin, core.QFileSystemWatcher):
    """Interface for monitoring files and directories for modifications."""

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
