from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


IteratorFlagStr = Literal[
    "none",
    "subdirectories",
    "follow_symlinks",
]

ITERATOR_FLAG: bidict[IteratorFlagStr, core.QDirIterator.IteratorFlag] = bidict(
    none=core.QDirIterator.IteratorFlag.NoIteratorFlags,
    subdirectories=core.QDirIterator.IteratorFlag.Subdirectories,
    follow_symlinks=core.QDirIterator.IteratorFlag.FollowSymlinks,
)


class DirIterator(core.QDirIterator):
    """Iterator for directory entrylists."""

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
