# -*- coding: utf-8 -*-

import pathlib

from qtpy import QtCore


class FileInfo(QtCore.QFileInfo):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], pathlib.Path):
            super().__init__(str(args[0]))
        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"FileInfo({self.absoluteFilePath()!r})"


if __name__ == "__main__":
    p = pathlib.Path.home()
    f = FileInfo(p)
