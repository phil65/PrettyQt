# -*- coding: utf-8 -*-

import pathlib

from qtpy import QtCore


class Dir(QtCore.QDir):
    def __repr__(self):
        return f"Dir('{self.absolutePath()}')"

    def __str__(self):
        return self.absolutePath()

    def __reduce__(self):
        return (self.__class__, (self.absolutePath(),))

    def __truediv__(self, other: str):
        path = self.to_path() / other
        return Dir(str(path))

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.absolutePath())
