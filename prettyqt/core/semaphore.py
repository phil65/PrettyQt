from __future__ import annotations

from collections.abc import Generator
import contextlib

from prettyqt.qt import QtCore


class Semaphore(QtCore.QSemaphore):
    @contextlib.contextmanager
    def acquire_resources(self, n: int = 1) -> Generator[bool, None, None]:
        yield self.tryAcquire(n)
        self.release(n)
