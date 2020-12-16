from __future__ import annotations

import contextlib
import pathlib
from typing import Literal, Union

from qtpy import QtCore

from prettyqt.utils import bidict


LOCK_ERROR = bidict(
    none=QtCore.QLockFile.NoError,
    lock_failed=QtCore.QLockFile.LockFailedError,
    permission=QtCore.QLockFile.PermissionError,
    unknown=QtCore.QLockFile.UnknownError,
)

LockErrorStr = Literal["none", "lock_failed", "permission", "unknown"]


class LockFile(QtCore.QLockFile):
    def __init__(self, path: Union[str, pathlib.Path]):
        super().__init__(str(path))

    def get_error(self) -> LockErrorStr:
        return LOCK_ERROR.inverse[self.error()]

    @contextlib.contextmanager
    def lock_file(self):
        self.lock()
        yield self
        self.unlock()
