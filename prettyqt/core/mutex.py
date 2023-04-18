from __future__ import annotations

import contextlib

from prettyqt.qt import QtCore


class Mutex(QtCore.QMutex):
    @contextlib.contextmanager
    def lock_mutex(self, timeout: int | None = None):
        if timeout is None:
            timeout = -1
        yield self.tryLock(timeout)
        self.unlock()
