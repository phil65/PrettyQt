from __future__ import annotations

import contextlib
import os
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, datatypes


LockErrorStr = Literal["none", "lock_failed", "permission", "unknown"]

LOCK_ERROR: bidict[LockErrorStr, QtCore.QLockFile.LockError] = bidict(
    none=QtCore.QLockFile.LockError.NoError,
    lock_failed=QtCore.QLockFile.LockError.LockFailedError,
    permission=QtCore.QLockFile.LockError.PermissionError,
    unknown=QtCore.QLockFile.LockError.UnknownError,
)


class LockFile(QtCore.QLockFile):
    """Locking between processes using a file."""

    def __init__(self, path: datatypes.PathType):
        super().__init__(os.fspath(path))

    def get_error(self) -> LockErrorStr:
        return LOCK_ERROR.inverse[self.error()]

    @contextlib.contextmanager
    def lock_file(self):
        self.lock()
        yield self
        self.unlock()
