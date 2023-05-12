from __future__ import annotations

from collections.abc import Callable
import functools
import logging

from prettyqt import core
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)


class Signals(core.Object):
    finished = core.Signal()
    error = core.Signal(Exception)
    result = core.Signal(object)
    progress = core.Signal(int)


class Worker(core.Runnable):
    """Worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    Arguments:
        fn:     The function callback to run on this worker thread.
                Supplied args and kwargs will be passed through to the runner.
        args:   Arguments to pass to the callback function
        kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn: Callable, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.keyword_args = kwargs
        self.signals = Signals()
        super().__init__()

        # Add the callback to our kwargs
        # self.keyword_args["progress_callback"] = self.signals.progress

    @core.Slot()
    def run(self):
        """Initialise the runner function with passed args, kwargs."""
        try:
            result = self.fn(*self.args, **self.keyword_args)
            self.signals.result.emit(result)
            self.signals.finished.emit()
        except Exception as e:
            logger.exception(e)
            self.signals.error.emit(e)


class GeneratorWorker(Worker):
    @core.Slot()
    def run(self):
        try:
            for result in self.fn(*self.args, **self.keyword_args):
                self.signals.result.emit(result)
            self.signals.finished.emit()
        except Exception as e:
            logger.exception(e)
            self.signals.error.emit(e)


def run_async(func: Callable) -> Callable:
    @functools.wraps(func)
    def async_func(*args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        pool = ThreadPool.globalInstance()
        pool.start(worker)

    return async_func


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
