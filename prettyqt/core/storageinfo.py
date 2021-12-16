from __future__ import annotations

import os
import pathlib

from prettyqt.qt import QtCore
from prettyqt.utils import types


class StorageInfo(QtCore.QStorageInfo):
    def __init__(
        self,
        path: QtCore.QStorageInfo | QtCore.QDir | types.PathType | None = None,
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
        return f"{type(self).__name__}({self.rootPath()!r})"

    def get_device(self) -> str:
        return bytes(self.device()).decode()

    def get_file_system_type(self) -> str:
        return bytes(self.fileSystemType()).decode()

    def get_subvolume(self) -> str:
        return bytes(self.subvolume()).decode()

    def get_root_path(self) -> pathlib.Path:
        return pathlib.Path(self.rootPath())

    @classmethod
    def get_root(cls) -> StorageInfo:
        return cls(cls.root())

    @classmethod
    def get_mounted_volumes(cls) -> list[StorageInfo]:
        return [cls(i) for i in cls.mountedVolumes()]
