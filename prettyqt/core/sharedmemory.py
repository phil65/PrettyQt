from __future__ import annotations

from typing import Literal

from prettyqt import core
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
    SharedMemoryErrorStr, core.QSharedMemory.SharedMemoryError
] = bidict(
    none=core.QSharedMemory.SharedMemoryError.NoError,
    permission_denied=core.QSharedMemory.SharedMemoryError.PermissionDenied,
    invalid_size=core.QSharedMemory.SharedMemoryError.InvalidSize,
    key_error=core.QSharedMemory.SharedMemoryError.KeyError,
    already_exists=core.QSharedMemory.SharedMemoryError.AlreadyExists,
    not_found=core.QSharedMemory.SharedMemoryError.NotFound,
    lock_error=core.QSharedMemory.SharedMemoryError.LockError,
    out_of_resources=core.QSharedMemory.SharedMemoryError.OutOfResources,
    unknown=core.QSharedMemory.SharedMemoryError.UnknownError,
)


class SharedMemory(core.ObjectMixin, core.QSharedMemory):
    """Access to a shared memory segment."""

    def __repr__(self):
        return get_repr(self, self.key())

    def __reduce__(self):
        return type(self), (self.key())

    def get_error(self) -> SharedMemoryErrorStr:
        return SHARED_MEMORY_ERROR.inverse[self.error()]
