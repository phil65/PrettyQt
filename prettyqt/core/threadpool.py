from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class ThreadPool(core.ObjectMixin, QtCore.QThreadPool):
    def __contains__(self, other: QtCore.QThread):
        return self.contains(other)

    def get_thread_priority(self) -> core.thread.PriorityStr:
        return core.thread.PRIORITY.inverse[self.priority()]

    def set_thread_priority(self, priority: core.thread.PriorityStr):
        prio = core.thread.PRIORITY[self.threadPriority()]
        self.setThreadPriority(prio)


if __name__ == "__main__":
    pool = ThreadPool()
