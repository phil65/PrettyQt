from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from collections.abc import Generator


class Semaphore(QtCore.QSemaphore):
    """General counting semaphore."""

    @contextlib.contextmanager
    def acquire_resources(self, n: int = 1) -> Generator[bool, None, None]:
        yield self.tryAcquire(n)
        self.release(n)
