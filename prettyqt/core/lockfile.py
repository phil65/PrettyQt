from __future__ import annotations

import contextlib
import os
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, types


LOCK_ERROR = bidict(
    none=QtCore.QLockFile.LockError.NoError,
    lock_failed=QtCore.QLockFile.LockError.LockFailedError,
    permission=QtCore.QLockFile.LockError.PermissionError,
    unknown=QtCore.QLockFile.LockError.UnknownError,
)

LockErrorStr = Literal["none", "lock_failed", "permission", "unknown"]


class LockFile(QtCore.QLockFile):
    def __init__(self, path: types.PathType):
        super().__init__(os.fspath(path))

    def get_error(self) -> LockErrorStr:
        return LOCK_ERROR.inverse[self.error()]

    @contextlib.contextmanager
    def lock_file(self):
        self.lock()
        yield self
        self.unlock()
