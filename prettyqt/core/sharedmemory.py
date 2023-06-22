from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


SharedMemoryErrorStr = Literal[
    "none",
    "permission_denied",
    "invalid_size",
    "key_error",
    "already_exists",
    "not_found",
    "lock_error",
    "out_of_resources",
    "unknown",
]

SHARED_MEMORY_ERROR: bidict[
    SharedMemoryErrorStr, QtCore.QSharedMemory.SharedMemoryError
] = bidict(
    none=QtCore.QSharedMemory.SharedMemoryError.NoError,
    permission_denied=QtCore.QSharedMemory.SharedMemoryError.PermissionDenied,
    invalid_size=QtCore.QSharedMemory.SharedMemoryError.InvalidSize,
    key_error=QtCore.QSharedMemory.SharedMemoryError.KeyError,
    already_exists=QtCore.QSharedMemory.SharedMemoryError.AlreadyExists,
    not_found=QtCore.QSharedMemory.SharedMemoryError.NotFound,
    lock_error=QtCore.QSharedMemory.SharedMemoryError.LockError,
    out_of_resources=QtCore.QSharedMemory.SharedMemoryError.OutOfResources,
    unknown=QtCore.QSharedMemory.SharedMemoryError.UnknownError,
)


class SharedMemory(core.ObjectMixin, QtCore.QSharedMemory):
    def __repr__(self):
        return get_repr(self, self.key())

    def __reduce__(self):
        return type(self), (self.key())

    def get_error(self) -> SharedMemoryErrorStr:
        return SHARED_MEMORY_ERROR.inverse[self.error()]
