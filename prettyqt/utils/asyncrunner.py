# modified version of https://github.com/nicoddemus/qt-async-threads/

from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Generator,
    Iterable,
    Iterator,
)
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
import dataclasses
import functools
import itertools
import logging
import os
import threading
import time
from typing import Any, ParamSpec, Self, TypeVar, cast

from prettyqt import core


log = logging.getLogger(__name__)

Params = ParamSpec("Params")
T = TypeVar("T")


class AsyncRunner:
    """A runner which runs long-lasting functions using a thread pool."""

    def __init__(self, max_threads: int | None = None):
        super().__init__()
        self._max_threads = max_threads or os.cpu_count() or 1
        self._pool = ThreadPoolExecutor(max_workers=max_threads)

        # Keep track of running tasks,
        # mostly to know if we are idle or not.
        self._running_tasks: list[_AsyncTask] = []

        # This signaller object is used to signal to us when a future running
        # in another thread finishes. Thanks to Qt's queued connections,
        # signals can be safely emitted from separate threads and are queued
        # to run in the same thread as the object receiving it lives (the main
        # thread in our case).
        self._signaller = _FutureDoneSignaller()
        self._signaller.future_done_signal.connect(self._resume_coroutine)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object):
        self.close()

    def to_sync(
        self, async_func: Callable[..., Coroutine[Any, Any, None]]
    ) -> Callable[..., None]:
        """Return new sync function.

        Return a new sync function that will start its coroutine using
        ``start_coroutine`` when called, returning immediately.
        Use to connect Qt signals to async functions

        Arguments:
            async_func: Async Qt Slot

        Returns:
            new sync function

        ### Example:
        ```py
        dl_btn.clicked.connect(self.runner.to_sync(self._on_dl_btn_clicked)
        ...
        search_response = await self.runner.run(requests.get, api_url)
        ```
        """

        @functools.wraps(async_func)
        def func(*args: object, **kwargs: object):
            gen = async_func(*args, **kwargs)
            self.start_coroutine(gen)

        return func

    @property
    def max_threads(self) -> int:
        """Return the maximum number of threads used by the internal threading pool."""
        return self._max_threads

    def is_idle(self) -> bool:
        return len(self._running_tasks) == 0

    def close(self):
        self._pool.shutdown(wait=True, cancel_futures=True)

    async def run(
        self, func: Callable[Params, T], *args: Params.args, **kwargs: Params.kwargs
    ) -> T | None:
        """Run the given function in a thread.

        While it is running, yields
        the control back to the Qt event loop.

        When the thread finishes, this async function resumes, returning
        the return value from the function.

        Arguments:
            func: Callable to run in a thrad
            args: arguments passed to Callable
            kwargs: keyword arguments passed to Callable

        Returns:
            return value from function
        """
        funcs = [functools.partial(func, *args, **kwargs)]
        async for result in self.run_parallel(funcs):
            return result
        return None

    async def run_parallel(  # type:ignore[override]
        self, funcs: Iterable[Callable[[], T]]
    ) -> AsyncIterator[T]:
        """Run functions in parallel.

        Run functions in parallel without arguments, yielding results as they get ready.
        (use ``functools.partial`` as necessary)

        Arguments:
            funcs: Sequence of Functions to call.
        """
        # We submit the functions in batches to avoid overloading the pool,
        # which can cause other coroutines to stall.
        # For example, Autofit works by executing 1000s of small functions,
        # which might take a few ms each. If we submitted all those 1000s of functions
        # at once (at the time ``run_parallel`` is called), then other coroutines
        # that try to submit functions to execute in threads would only be resumed
        # much later, causing a noticeable slow down in the application.
        batch_size = max(self._max_threads // 2, 1)
        for function_batch in itertools.batched(funcs, batch_size):
            # Submit all functions from the current batch to the thread pool,
            # using the _AsyncTask to track the futures and await when they finish.
            task = _AsyncTask({self._pool.submit(f) for f in function_batch})
            self._running_tasks.append(task)
            for future in task.futures:
                future.add_done_callback(
                    functools.partial(self._on_task_future_done, task=task)
                )
            try:
                # We wait until all functions in this batch have finished
                # until we submit the next batch. This is not 100% optimal
                # but ensures we get a fairer share of the pool.
                while task.futures:
                    await task
                    for result in task.pop_done_futures():
                        yield result
            finally:
                task.shutdown()
                self._running_tasks.remove(task)

    def _on_future_done(
        self,
        future: Future,
        *,
        coroutine: Coroutine[Any, Any, Any],
    ):
        """Called when a ``Future`` that was submitted to the thread pool finishes.

        This function is called from a separate thread, so we emit the signal
        of the internal ``_signaller``, which thanks to Qt's queued connections feature,
        will post the event to the main loop, and it will be processed there.

        Arguments:
            future: future which finished
            coroutine: Coroutine
        """
        self._signaller.future_done_signal.emit(future, coroutine)

    def _on_task_future_done(self, future: Future, *, task: _AsyncTask):
        """Called when a ``Future`` belonging to a ``_AsyncTask`` has finished.

        Similar to ``_on_future_done``, this emits a signal so the coroutine is resumed
        in the main thread.

        Arguments:
            future: future which finished
            task:  Async Task
        """
        # At this point, we want to get the coroutine associated with the task, and resume
        # its execution in the main loop, but we must take care bc this callback is called
        # from another thread, and it may be called multiple times in succession, but we
        # want only **one** event to be sent, that's
        # why we use ``pop_coroutine``, which is lock-protected and will return
        # the coroutine and set it to None, so next calls of this method will get ``None``
        # and won't trigger the event again.
        if coroutine := task.pop_coroutine():
            self._signaller.future_done_signal.emit(future, coroutine)

    def _resume_coroutine(
        self,
        future: Future,
        coroutine: Coroutine[Any, Any, Any],
    ):
        """Resume paused coroutine.

        Slots connected to our internal ``_signaller`` object,
        called in the main thread after a future finishes, resuming the paused coroutine.

        Arguments:
            future: not used
            coroutine: coroutine to resume
        """
        assert threading.current_thread() is threading.main_thread()
        self.start_coroutine(coroutine)

    def start_coroutine(self, coroutine: Coroutine):
        """Start the coroutine, and returns immediately.

        Arguments:
            coroutine: coroutine to start
        """
        # Note: this function will also be called to resume a paused coroutine that was
        # waiting for a thread to finish (by ``_resume_coroutine``).
        with suppress(StopIteration):
            value = coroutine.send(None)
            if isinstance(value, _AsyncTask):
                # At this point, return control to the event loop; when one
                # of the futures running in the task finishes, it will resume the
                # coroutine back in the main thread.
                value.coroutine = coroutine
                return
            raise ValueError(value)

    def run_coroutine(self, coroutine: Coroutine[Any, Any, T]) -> T:
        """Start the coroutine.

        Starts the coroutine, doing a busy loop while waiting for it to complete,
        returning then the result.

        Arguments:
            coroutine: coroutine to start

        Note: see warning in AbstractAsyncRunner about when to use this function.
        """
        result: T | None = None
        exception: Exception | None = None
        completed = False

        async def wrapper():
            nonlocal result, exception, completed
            try:
                result = await coroutine
            except Exception as e:  # noqa: BLE001
                exception = e
            completed = True

        self.start_coroutine(wrapper())
        while not completed:
            core.CoreApplication.processEvents()
            time.sleep(0.01)

        if exception is not None:
            raise exception
        return cast(T, result)


@dataclasses.dataclass
class _AsyncTask(Awaitable[None]):
    """Awaitable that is propagated up the async stack, containing running futures.

    It "awaits" while all futures are processing, and will
    stop and return once any of them complete.
    """

    futures: set[Future]
    coroutine: Coroutine | None = None
    _lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __await__(self) -> Generator[Any, None, None]:
        if any(x for x in self.futures if x.done()):
            return None
        else:
            yield self

    def pop_done_futures(self) -> Iterator[Any]:
        """Yield done futures, removing them from the ``futures`` simultaniously."""
        for future in list(self.futures):
            if future.done():
                self.futures.discard(future)
                yield future.result()

    def pop_coroutine(self) -> Coroutine | None:
        """Return current coroutine.

        Returns the current coroutine associated with this object, while
        also setting the ``coroutine`` attribute to ``None``. This
        is meant to be called from multiple threads, in a way that only
        one of them will be able to obtain the coroutine object, while the
        others will get ``None``.
        """
        with self._lock:
            coroutine = self.coroutine
            self.coroutine = None
            return coroutine

    def shutdown(self):
        """Cancel any running futures and clears up its attributes."""
        msg = (
            "Should always be called from ``run_parallel``, "
            "at which point this should not have a coroutine associated"
        )
        assert self.coroutine is None, msg
        while self.futures:
            future = self.futures.pop()
            future.cancel()


class _FutureDoneSignaller(core.Object):
    """Used to emit a signal to the main thread when a future finishes in another."""

    # This emits(Future, Coroutine). We need to use ``object`` as the
    # second parameter because Qt doesn't allow us to use an ABC class there it seems.
    future_done_signal = core.Signal(Future, object)


if __name__ == "__main__":
    from pathlib import Path
    from urllib.parse import urlsplit

    import requests
    from requests import Response
    from requests.exceptions import ConnectionError as ConnError

    from prettyqt import widgets

    class Window(widgets.Widget):
        def __init__(self, directory: Path):
            super().__init__()

            self.setWindowTitle("Cat Downloader")
            self.directory = directory
            self._cancelled = False

            # Build controls.
            self.count_spin = widgets.SpinBox(value=5, minimum=1)
            self.progress_label = widgets.Label("Idle, click below to start downloading")
            self.download_button = widgets.PushButton(
                "Download", clicked=self.on_download_button_clicked
            )
            self.stop_button = widgets.PushButton(
                "Stop", enabled=False, clicked=self.on_cancel_button_clicked
            )

            layout = widgets.FormLayout(self)
            layout.addRow("How many cats?", self.count_spin)
            layout.addRow("Status", self.progress_label)
            layout.addRow(self.download_button)
            layout.addRow(self.stop_button)

        async def on_download_button_clicked(self, checked: bool = False):
            self.progress_label.setText("Searching...")
            self.download_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            self._cancelled = False
            downloaded_count = 0

            def download_one() -> Response:
                # Search.
                search_response = requests.get(
                    "https://api.thecatapi.com/v1/images/search"
                )
                search_response.raise_for_status()

                # Download.
                url = search_response.json()[0]["url"]
                return requests.get(url)

            try:
                functions = [download_one for _ in range(self.count_spin.value())]
                async for response in widgets.app().run_parallel(functions):
                    # Save the contents of the image to a file.
                    parts = urlsplit(response.url)
                    path = (
                        self.directory
                        / f"{downloaded_count:02d}_cat{Path(parts.path).suffix}"
                    )
                    path.write_bytes(response.content)
                    downloaded_count += 1

                    # Show progress.
                    self.progress_label.setText(f"Downloaded {path.name}")
                    widgets.app().processEvents()
                    if self._cancelled:
                        widgets.MessageBox.information(
                            self, "Cancelled", "Download cancelled"
                        )
                        return
            except ConnError as e:
                widgets.MessageBox.critical(self, "Error", e)
                return
            finally:
                self.progress_label.setText(f"Done, {downloaded_count} cats downloaded")
                self.download_button.setEnabled(True)
                self.stop_button.setEnabled(False)

        def on_cancel_button_clicked(self):
            self._cancelled = True

    app = widgets.app()
    win = Window(Path(__file__).parent)
    win.show()
    app.exec()
