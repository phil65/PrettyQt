"""Binding-agnostic `asyncio` integration for Qt applications.

Provides:
- `AsyncBridge`: runs a standard `asyncio` event loop on a dedicated daemon
  thread with context-preserving marshaling (`contextvars`) in both directions
  between Qt's GUI thread and the async loop. Works identically on PyQt6 and
  PySide6 with zero third-party dependencies, full socket/HTTP/subprocess
  support, and no modal-dialog `.exec()` re-entrancy issues.
- `schedule_coroutine()`: schedules an `asyncio` coroutine on the running
  main-thread event loop (e.g. `qasync` / `qtinter` / `QtAsyncio`) when
  present, or on the shared `AsyncBridge` otherwise, tracking live tasks and
  surfacing unhandled exceptions.
- `run_in_gui_thread()`: awaits execution of a callable on Qt's main thread.
- `wait_for_signal()`: awaits the next emission of any Qt signal as a Future.
- `enable_async_slots()` / `disable_async_slots()`: opt-in hook allowing
  `async def` functions to be connected directly to Qt signals.
- `run_async()`: unified entry point supporting `qasync`, `qtinter`,
  `qtasyncio`, or `bridge` (with `"auto"` selection).
"""

import asyncio
import concurrent.futures
import contextlib
import contextvars
import importlib.util
import inspect
import logging
import threading
from typing import TYPE_CHECKING, Any, Literal, Self
import weakref

from prettyqt.qt import QtCore
from prettyqt.utils import signalhooks


if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine, Generator


logger = logging.getLogger(__name__)

AsyncBackendStr = Literal["auto", "qasync", "qtinter", "qtasyncio", "bridge"]

# Keep strong references to scheduled main-thread tasks until completion so
# Python does not garbage-collect running tasks mid-flight.
_background_tasks: set[asyncio.Task[Any]] = set()
_loop_to_bridge: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, AsyncBridge] = (
    weakref.WeakKeyDictionary()
)


class _GuiDispatcher(QtCore.QObject):
    """QObject living on the Qt main thread that executes marshaled callbacks."""

    _invoke = QtCore.Signal(object)

    def __init__(self) -> None:
        super().__init__()
        app = QtCore.QCoreApplication.instance()
        if app is not None and self.thread() != app.thread():
            self.moveToThread(app.thread())
        self._invoke.connect(self._execute, QtCore.Qt.ConnectionType.QueuedConnection)

    def _execute(self, payload: tuple[Any, ...]) -> None:
        ctx, fn, args, kwargs, loop, fut = payload
        if fut.cancelled():
            return
        try:
            result = ctx.run(fn, *args, **kwargs)
        except BaseException as exc:  # noqa: BLE001
            if not loop.is_closed():
                loop.call_soon_threadsafe(_set_exception_if_pending, fut, exc)
        else:
            if not loop.is_closed():
                loop.call_soon_threadsafe(_set_result_if_pending, fut, result)

    _execute._prettyqt_skip_trace = True  # ty: ignore[missing-attribute]


def _set_result_if_pending(fut: asyncio.Future[Any], result: Any) -> None:
    if not fut.done():
        fut.set_result(result)


def _set_exception_if_pending(fut: asyncio.Future[Any], exc: BaseException) -> None:
    if not fut.done():
        fut.set_exception(exc)


def _report_future_error(
    fut: asyncio.Future[Any] | concurrent.futures.Future[Any],
    on_error: Callable[[BaseException], Any] | None = None,
) -> None:
    if fut.cancelled():
        return
    exc = fut.exception()
    if exc is None:
        return
    if on_error is not None:
        on_error(exc)
    else:
        logger.error("Unhandled exception in async slot", exc_info=exc)


class AsyncBridge:
    """Runs a standard `asyncio` loop in a background thread bridged to Qt.

    Both `submit()` (Qt -> asyncio) and `call_in_gui_thread()` (asyncio -> Qt)
    propagate `contextvars.Context`, preserving OpenTelemetry spans and any
    other context variables seamlessly across thread boundaries.
    """

    def __init__(self, *, debug: bool = False) -> None:
        self._debug = debug
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._dispatcher: _GuiDispatcher | None = None
        self._started = threading.Event()
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._loop is not None and self._loop.is_running()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None or not self._loop.is_running():
            msg = "AsyncBridge is not running; call start() first."
            raise RuntimeError(msg)
        return self._loop

    def start(self) -> Self:
        """Start the background `asyncio` event loop thread."""
        with self._lock:
            if self.is_running:
                return self
            self._started.clear()
            if QtCore.QCoreApplication.instance() is not None:
                self._dispatcher = _GuiDispatcher()
            self._thread = threading.Thread(
                target=self._run_loop,
                name="prettyqt-asyncio",
                daemon=True,
            )
            self._thread.start()
        self._started.wait()
        return self

    def stop(self, timeout: float = 5.0) -> None:
        """Cancel pending tasks and stop the background event loop thread."""
        with self._lock:
            loop = self._loop
            thread = self._thread
            if loop is None:
                return
            if loop.is_running():
                loop.call_soon_threadsafe(self._cancel_all_and_stop, loop)
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=timeout)
        with self._lock:
            self._loop = None
            self._thread = None
            self._dispatcher = None

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(self, *exc_info: object) -> None:
        self.stop()

    def _run_loop(self) -> None:
        loop = asyncio.new_event_loop()
        loop.set_debug(self._debug)
        asyncio.set_event_loop(loop)
        self._loop = loop
        _loop_to_bridge[loop] = self
        loop.call_soon(self._started.set)
        try:
            loop.run_forever()
        finally:
            try:
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                if pending:
                    loop.run_until_complete(
                        asyncio.gather(*pending, return_exceptions=True)
                    )
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.run_until_complete(loop.shutdown_default_executor())
            finally:
                loop.close()

    @staticmethod
    def _cancel_all_and_stop(loop: asyncio.AbstractEventLoop) -> None:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()

    def submit[T](
        self,
        coro: Coroutine[Any, Any, T],
        *,
        context: contextvars.Context | None = None,
        on_error: Callable[[BaseException], Any] | None = None,
    ) -> concurrent.futures.Future[T]:
        """Submit a coroutine to the background loop, preserving `contextvars`."""
        loop = self.loop
        ctx = contextvars.copy_context() if context is None else context
        result_fut: concurrent.futures.Future[T] = concurrent.futures.Future()

        def _start() -> None:
            if result_fut.cancelled():
                coro.close()
                return
            task = loop.create_task(coro, context=ctx)

            def _on_done(done_task: asyncio.Task[T]) -> None:
                if result_fut.done():
                    return
                if done_task.cancelled():
                    result_fut.cancel()
                elif (exc := done_task.exception()) is not None:
                    result_fut.set_exception(exc)
                else:
                    result_fut.set_result(done_task.result())

            task.add_done_callback(_on_done)

        if on_error is not None:
            result_fut.add_done_callback(lambda f: _report_future_error(f, on_error))
        loop.call_soon_threadsafe(_start)
        return result_fut

    def call_in_gui_thread[T](
        self, fn: Callable[..., T], *args: Any, **kwargs: Any
    ) -> asyncio.Future[T]:
        """Marshal `fn(*args, **kwargs)` onto the Qt main thread and await its result."""
        running_loop = asyncio.get_running_loop()
        fut: asyncio.Future[T] = running_loop.create_future()
        app = QtCore.QCoreApplication.instance()
        if app is None or QtCore.QThread.currentThread() == app.thread():
            try:
                fut.set_result(fn(*args, **kwargs))
            except BaseException as exc:  # noqa: BLE001
                fut.set_exception(exc)
            return fut
        if self._dispatcher is None:
            msg = "No QCoreApplication available for GUI thread dispatch."
            raise RuntimeError(msg)
        ctx = contextvars.copy_context()
        self._dispatcher._invoke.emit((ctx, fn, args, kwargs, running_loop, fut))
        return fut


_default_bridge: AsyncBridge | None = None
_bridge_lock = threading.Lock()


def get_async_bridge(*, auto_start: bool = True) -> AsyncBridge:
    """Return the process-wide `AsyncBridge`, starting it lazily by default."""
    global _default_bridge
    with _bridge_lock:
        if _default_bridge is None:
            _default_bridge = AsyncBridge()
        bridge = _default_bridge
    if auto_start and not bridge.is_running:
        bridge.start()
        app = QtCore.QCoreApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(stop_async_bridge)
    return bridge


def stop_async_bridge() -> None:
    """Stop and clear the process-wide `AsyncBridge` if running."""
    global _default_bridge
    with _bridge_lock:
        bridge = _default_bridge
        _default_bridge = None
    if bridge is not None:
        bridge.stop()


def schedule_coroutine[T](
    coro: Coroutine[Any, Any, T],
    *,
    loop: asyncio.AbstractEventLoop | None = None,
    on_error: Callable[[BaseException], Any] | None = None,
    use_bridge: bool = True,
) -> asyncio.Task[T] | concurrent.futures.Future[T]:
    """Schedule a coroutine onto the active `asyncio` loop or `AsyncBridge`.

    - If a running `asyncio` loop exists on the current thread (or `loop` is
      passed), creates a tracked `asyncio.Task` (preserving `contextvars` and
      preventing premature GC).
    - Otherwise, if `use_bridge` is True, submits to the shared `AsyncBridge`
      (preserving `contextvars` across the thread boundary).
    """
    target_loop = loop
    if target_loop is None:
        with contextlib.suppress(RuntimeError):
            target_loop = asyncio.get_running_loop()

    if target_loop is not None:
        task: asyncio.Task[T] = target_loop.create_task(coro)
        _background_tasks.add(task)

        def _cleanup(done: asyncio.Task[T]) -> None:
            _background_tasks.discard(done)
            _report_future_error(done, on_error)

        task.add_done_callback(_cleanup)
        return task

    if not use_bridge:
        coro.close()
        msg = "No running asyncio event loop and use_bridge=False."
        raise RuntimeError(msg)

    bridge = get_async_bridge(auto_start=True)
    fut = bridge.submit(coro)
    fut.add_done_callback(lambda f: _report_future_error(f, on_error))
    return fut


async def run_in_gui_thread[T](fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Execute `fn(*args, **kwargs)` on Qt's main GUI thread and await the result."""
    app = QtCore.QCoreApplication.instance()
    if app is None or QtCore.QThread.currentThread() == app.thread():
        return fn(*args, **kwargs)
    loop = asyncio.get_running_loop()
    bridge = _loop_to_bridge.get(loop) or get_async_bridge(auto_start=True)
    return await bridge.call_in_gui_thread(fn, *args, **kwargs)


async def wait_for_signal(
    signal: Any,
    *,
    timeout: float | None = None,
) -> Any:
    """Await the next emission of a Qt signal.

    Returns `None` for 0-arg signals, the single argument for 1-arg signals,
    or a tuple of arguments for multi-arg signals. Safe across both main-thread
    loops (`qasync`/`qtinter`) and `AsyncBridge` worker threads.
    """
    loop = asyncio.get_running_loop()
    fut: asyncio.Future[Any] = loop.create_future()

    def _on_emit(*args: Any) -> None:
        value: Any
        if not args:
            value = None
        elif len(args) == 1:
            value = args[0]
        else:
            value = args
        if not loop.is_closed():
            loop.call_soon_threadsafe(_set_result_if_pending, fut, value)

    _on_emit._prettyqt_skip_trace = True  # ty: ignore[missing-attribute]

    # Connect and disconnect on Qt's main thread so cross-thread calls from
    # `AsyncBridge` never race with QObject connection lists on PyQt6/PySide6.
    conn = await run_in_gui_thread(signal.connect, _on_emit)
    try:
        if timeout is not None:
            return await asyncio.wait_for(fut, timeout=timeout)
        return await fut
    finally:
        with contextlib.suppress(RuntimeError, TypeError):
            await run_in_gui_thread(signal.disconnect, conn)


class AsyncSlotHook:
    """SignalHook that schedules `async def` slots onto `asyncio` automatically."""

    priority: int = 50

    def __init__(self, *, on_error: Callable[[BaseException], Any] | None = None) -> None:
        self._on_error = on_error

    def wrap_slot(
        self,
        signal_info: signalhooks.SignalInfo,
        slot: Callable[..., Any],
    ) -> Callable[..., Any] | None:
        if not inspect.iscoroutinefunction(slot):
            return None
        on_error = self._on_error

        def _invoke(target: Callable[..., Any], args: tuple[Any, ...]) -> Any:
            return schedule_coroutine(target(*args), on_error=on_error)

        return signalhooks.make_safe_slot_wrapper(slot, _invoke)

    def on_emit(
        self, signal_info: signalhooks.SignalInfo, args: tuple[Any, ...]
    ) -> contextlib.AbstractContextManager[Any] | None:
        return None


_active_async_hook: AsyncSlotHook | None = None


def enable_async_slots(
    *, on_error: Callable[[BaseException], Any] | None = None
) -> AsyncSlotHook:
    """Enable connecting `async def` functions directly to Qt signals."""
    global _active_async_hook
    manager = signalhooks.get_hook_manager()
    if _active_async_hook is not None:
        manager.unregister(_active_async_hook)
    hook = AsyncSlotHook(on_error=on_error)
    manager.register(hook)
    _active_async_hook = hook
    return hook


def disable_async_slots() -> None:
    """Disable automatic scheduling of `async def` slots connected to Qt signals."""
    global _active_async_hook
    if _active_async_hook is not None:
        signalhooks.get_hook_manager().unregister(_active_async_hook)
        _active_async_hook = None


@contextlib.contextmanager
def async_slots_enabled(
    *, on_error: Callable[[BaseException], Any] | None = None
) -> Generator[AsyncSlotHook]:
    """Context manager enabling `async def` signal connections temporarily."""
    hook = enable_async_slots(on_error=on_error)
    try:
        yield hook
    finally:
        disable_async_slots()


def _resolve_backend(backend: AsyncBackendStr) -> AsyncBackendStr:
    if backend != "auto":
        return backend
    for candidate in ("qasync", "qtinter"):
        if importlib.util.find_spec(candidate) is not None:
            return candidate
    return "bridge"


def run_async(
    coro: Coroutine[Any, Any, Any] | None = None,
    *,
    backend: AsyncBackendStr = "auto",
    keep_running: bool = True,
    quit_qapp: bool = True,
    handle_sigint: bool = False,
    debug: bool | None = None,
) -> int:
    """Run the Qt application alongside a real `asyncio` event loop.

    Backends:
    - `"auto"` (default): uses `qasync` if installed, else `qtinter` if
      installed, else `"bridge"` (`AsyncBridge` + `app.exec()`).
    - `"qasync"`: unified Qt + asyncio loop via `qasync.QEventLoop`.
    - `"qtinter"`: interleaved loop via `qtinter`.
    - `"qtasyncio"`: PySide6's built-in `PySide6.QtAsyncio.run()` (PySide6 only;
      note that socket/HTTP transports are not yet implemented in QtAsyncio).
    - `"bridge"`: zero-dependency `AsyncBridge` daemon thread + `app.exec()`.
    """
    chosen = _resolve_backend(backend)
    app = QtCore.QCoreApplication.instance()
    if app is None and chosen != "qtasyncio":
        msg = "No QCoreApplication / QApplication instance exists."
        raise RuntimeError(msg)

    match chosen:
        case "qtasyncio":
            from prettyqt.qt import QtAsyncio

            return QtAsyncio.run(
                coro=coro,
                keep_running=keep_running,
                quit_qapp=quit_qapp,
                handle_sigint=handle_sigint,
                debug=debug,
            )

        case "qasync":
            import qasync

            loop = qasync.QEventLoop(app)
            if debug is not None:
                loop.set_debug(debug)
            asyncio.set_event_loop(loop)
            with loop:
                if coro is not None:
                    if keep_running:
                        loop.create_task(coro)
                        loop.run_forever()
                    else:
                        loop.run_until_complete(coro)
                else:
                    loop.run_forever()
            return 0

        case "qtinter":
            import qtinter

            assert app is not None
            with qtinter.using_asyncio_from_qt():
                if coro is not None:
                    task = asyncio.ensure_future(coro)
                    if not keep_running:
                        task.add_done_callback(lambda _: app.quit())
                return app.exec()

        case "bridge":
            assert app is not None
            bridge = get_async_bridge(auto_start=True)
            if debug is not None:
                bridge.loop.set_debug(debug)
            try:
                if coro is not None:
                    fut = bridge.submit(coro)
                    if not keep_running:
                        fut.add_done_callback(
                            lambda _: QtCore.QMetaObject.invokeMethod(
                                app,
                                "quit",
                                QtCore.Qt.ConnectionType.QueuedConnection,
                            )
                        )
                return app.exec()
            finally:
                stop_async_bridge()

        case _:
            msg = f"Unknown async backend: {chosen!r}"
            raise ValueError(msg)
