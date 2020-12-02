# -*- coding: utf-8 -*-

import pathlib

from qtpy import QtCore


class Dir(QtCore.QDir):
    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return f"Dir({self.absolutePath()!r})"

    def __str__(self):
        return self.absolutePath()

    def __reduce__(self):
        return (self.__class__, (self.absolutePath(),))

    def __truediv__(self, other: str) -> pathlib.Path:
        path = self.to_path() / other
        return path

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.absolutePath())
