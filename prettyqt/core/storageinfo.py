from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Self

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class StorageInfo(QtCore.QStorageInfo):
    """Provides information about currently mounted storage and drives."""

    def __init__(
        self,
        path: QtCore.QStorageInfo | QtCore.QDir | datatypes.PathType | None = None,
    ):
        if path is None:
            super().__init__()
        else:
            if isinstance(path, os.PathLike):
                path = os.fspath(path)
            super().__init__(path)

    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.rootPath())

    def get_device(self) -> str:
        return self.device().data().decode()

    def get_file_system_type(self) -> str:
        return self.fileSystemType().data().decode()

    def get_subvolume(self) -> str:
        return self.subvolume().data().decode()

    def get_root_path(self) -> pathlib.Path:
        return pathlib.Path(self.rootPath())

    @classmethod
    def get_root(cls) -> Self:
        return cls(cls.root())

    @classmethod
    def get_mounted_volumes(cls) -> list[Self]:
        return [cls(i) for i in cls.mountedVolumes()]
