from __future__ import annotations

import pathlib

from qtpy import QtCore


class TemporaryDir(QtCore.QTemporaryDir):
    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return f"{type(self).__name__}({self.path()!r})"

    def __str__(self):
        return self.path()

    def __bool__(self):
        return self.isValid()

    def __truediv__(self, other: str) -> pathlib.Path:
        current = pathlib.Path(self.path())
        return current / other
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
