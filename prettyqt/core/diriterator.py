from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


ITERATOR_FLAG = bidict(
    none=QtCore.QDirIterator.IteratorFlag.NoIteratorFlags,
    subdirectories=QtCore.QDirIterator.IteratorFlag.Subdirectories,
    follow_symlinks=QtCore.QDirIterator.IteratorFlag.FollowSymlinks,
)

IteratorFlagStr = Literal[
    "none",
    "subdirectories",
    "follow_symlinks",
]


class DirIterator(QtCore.QDirIterator):
    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        raise StopIteration

    def get_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.filePath())

    def get_file_info(self) -> core.FileInfo:
        return core.FileInfo(self.fileInfo())


if __name__ == "__main__":
    it = core.DirIterator("C:/Intel")
    print(list(it))
