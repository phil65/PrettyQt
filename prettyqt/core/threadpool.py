from __future__ import annotations

from collections.abc import Callable
import functools
import logging
import inspect

from typing_extensions import Self

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

    def __getattr__(self, name: str) -> core.SignalInstance:
        attr = getattr(self.signals, name, None)
        if isinstance(attr, core.SignalInstance):
            return getattr(self.signals, name)
        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

    @core.Slot()
    def run(self):
        """Initialise the runner function with passed args, kwargs."""
        try:
            if inspect.isgeneratorfunction(self.fn):
                for result in self.fn(*self.args, **self.keyword_args):
                    self.signals.result.emit(result)
            else:
                result = self.fn(*self.args, **self.keyword_args)
                self.signals.result.emit(result)
            self.signals.finished.emit()
        except Exception as e:
            logger.exception(e)
            self.signals.error.emit(e)


def run_async(
    result_fn: Callable | None = None,
    finished_fn: Callable | None = None,
    progress_fn: Callable | None = None,
    error_fn: Callable | None = None,
):
    def inner(func: Callable) -> Callable:
        @functools.wraps(func)
        def async_func(*args, **kwargs):
            pool = ThreadPool.instance()
            pool.start_worker(
                func,
                args,
                kwargs,
                result_fn=result_fn,
                finished_fn=finished_fn,
                progress_fn=progress_fn,
                error_fn=error_fn,
            )

        return async_func

    return inner


class ThreadPool(core.ObjectMixin, QtCore.QThreadPool):
    """Note: signals only work correctly when exclusively using start_worker method."""

    __instance: Self | None = None  # a global instance

    job_num_updated = core.Signal(int)
    error_occured = core.Signal(Exception)
    busy_state_changed = core.Signal(bool)

    def __contains__(self, other: QtCore.QThread):
        return self.contains(other)

    def get_thread_priority(self) -> core.thread.PriorityStr:
        return core.thread.PRIORITY.inverse[self.threadPriority()]

    def set_thread_priority(self, priority: core.thread.PriorityStr):
        prio = core.thread.PRIORITY[priority]
        self.setThreadPriority(prio)

    @classmethod
    def instance(cls) -> Self:
        """Return global ThreadPool singleton. (globalInstance always returns Qt type)."""
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def start_worker(
        self,
        fn_or_worker: Callable | Worker,
        args: tuple | None = None,
        kwargs: dict | None = None,
        priority: int = 0,
        result_fn: Callable | None = None,
        finished_fn: Callable | None = None,
        progress_fn: Callable | None = None,
        error_fn: Callable | None = None,
    ):
        if isinstance(fn_or_worker, Callable):
            if args is None:
                args = ()
            if kwargs is None:
                kwargs = {}
            runnable = Worker(fn_or_worker, *args, **kwargs)
        else:
            runnable = fn_or_worker
        runnable.signals.finished.connect(self._on_job_ended)
        runnable.signals.error.connect(self._on_job_ended)
        runnable.signals.error.connect(self._on_exception)
        if result_fn:
            runnable.signals.result.connect(result_fn)
        if finished_fn:
            runnable.signals.finished.connect(finished_fn)
        if progress_fn:
            runnable.signals.progress.connect(progress_fn)
        if error_fn:
            runnable.signals.error.connect(error_fn)
        thread_count = self.activeThreadCount()
        if thread_count == 0:
            self.busy_state_changed.emit(True)
        self.job_num_updated.emit(thread_count + 1)  # + 1 because we didnt start yet.
        super().start(runnable, priority)

    def _on_job_ended(self):
        thread_count = self.activeThreadCount()
        if thread_count == 1:  # this is the last job
            self.busy_state_changed.emit(False)
        self.job_num_updated.emit(thread_count - 1)  # -1 because we didnt really end yet.

    def _on_exception(self, exception):
        self.error_occured.emit(exception)


if __name__ == "__main__":
    pool = ThreadPool()
