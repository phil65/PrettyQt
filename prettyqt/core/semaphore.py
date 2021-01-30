from __future__ import annotations

import contextlib

from prettyqt.qt import QtCore


class Semaphore(QtCore.QSemaphore):
    @contextlib.contextmanager
    def acquire_resources(self, n: int = 1):
        result = self.tryAcquire(n)
        yield result
        self.release(n)
