from __future__ import annotations

import os
import pathlib
from typing import Any

from prettyqt import core
from prettyqt.qt import QtCore


class FileInfo(QtCore.QFileInfo):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], os.PathLike):
            super().__init__(os.fspath(args[0]))
        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}({self.absoluteFilePath()!r})"

    def __str__(self):
        return self.absoluteFilePath()

    def __fspath__(self) -> str:
        return self.absoluteFilePath()

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.get_absolute_file_path(), attr)

    def __reduce__(self):
        return type(self), (self.absoluteFilePath(),)

    def get_dir(self) -> pathlib.Path:
        return pathlib.Path(self.dir().absolutePath())

    def get_absolute_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.absoluteFilePath())

    def get_birth_time(self) -> core.DateTime:
        return core.DateTime(self.birthTime())

    def get_metadata_change_time(self) -> core.DateTime:
        return core.DateTime(self.metadataChangeTime())

    def get_last_modified(self) -> core.DateTime:
        return core.DateTime(self.lastModified())

    def get_last_read(self) -> core.DateTime:
        return core.DateTime(self.lastRead())


if __name__ == "__main__":
    p = pathlib.Path.home()
    f = FileInfo(p)
