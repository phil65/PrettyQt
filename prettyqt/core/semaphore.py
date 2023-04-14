from __future__ import annotations

from collections.abc import Generator
import contextlib

from prettyqt.qt import QtCore


class Semaphore(QtCore.QSemaphore):
    @contextlib.contextmanager
    def acquire_resources(self, n: int = 1) -> Generator[bool, None, None]:
        result = self.tryAcquire(n)
        yield result
        self.release(n)
