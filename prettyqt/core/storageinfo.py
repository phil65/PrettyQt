from __future__ import annotations

import pathlib
from typing import List, Optional, Union

from qtpy import QtCore


class StorageInfo(QtCore.QStorageInfo):
    def __init__(
        self,
        path: Optional[Union[QtCore.QStorageInfo, QtCore.QDir, str, pathlib.Path]] = None,
    ):
        if path is not None:
            super().__init__(path)
        else:
            if isinstance(path, pathlib.Path):
                path = str(path)
            super().__init__()

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
    def get_mounted_volumes(cls) -> List[StorageInfo]:
        return [cls(i) for i in cls.mountedVolumes()]
