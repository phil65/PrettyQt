from __future__ import annotations

import os
import pathlib

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class TemporaryDir(QtCore.QTemporaryDir):
    """Creates a unique directory for temporary use."""

    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return get_repr(self, self.path())

    def __str__(self):
        return self.path()

    def __bool__(self):
        return self.isValid()

    def __fspath__(self) -> str:
        return self.path()

    def __truediv__(self, other: datatypes.PathType) -> pathlib.Path:
        current = pathlib.Path(self.path())
        return current / os.fspath(other)
        # new = current / other
        # if new.suffix == "":
        #     return core.Dir(new)
        # else:
        #     return core.File(new)

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.path())


if __name__ == "__main__":
    temp = TemporaryDir()
    new = temp / "test"
    print(new)
