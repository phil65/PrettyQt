import contextlib
from typing import TYPE_CHECKING, Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Generator


RecursionModeStr = Literal["non_recursive", "recursive"]

RECURSION_MODE: bidict[RecursionModeStr, QtCore.QReadWriteLock.RecursionMode] = bidict(
    non_recursive=QtCore.QReadWriteLock.RecursionMode.NonRecursive,
    recursive=QtCore.QReadWriteLock.RecursionMode.Recursive,
)


class ReadWriteLock(QtCore.QReadWriteLock):
    """Read-write locking between threads."""

    def __init__(
        self,
        recursion_mode: RecursionModeStr
        | QtCore.QReadWriteLock.RecursionMode = "non_recursive",
    ):
        super().__init__(RECURSION_MODE.get_enum_value(recursion_mode))

    @contextlib.contextmanager
    def lock_for_read(self, timeout: int | None = None) -> Generator[bool]:
        acquired = (
            self.tryLockForRead() if timeout is None else self.tryLockForRead(timeout)
        )
        try:
            yield acquired
        finally:
            if acquired:
                self.unlock()

    @contextlib.contextmanager
    def lock_for_write(self, timeout: int | None = None) -> Generator[bool]:
        acquired = (
            self.tryLockForWrite() if timeout is None else self.tryLockForWrite(timeout)
        )
        try:
            yield acquired
        finally:
            if acquired:
                self.unlock()
