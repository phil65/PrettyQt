"""OpenTelemetry instrumentation for Qt applications and PrettyQt."""

import contextlib
import functools
import inspect
import logging
import threading
import time
from typing import TYPE_CHECKING, Any, Self

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.telemetry import _otel
from prettyqt.utils import signalhooks


if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Mapping


logger = logging.getLogger(__name__)

DEFAULT_UI_EVENT_TYPES: frozenset[QtCore.QEvent.Type] = frozenset({
    QtCore.QEvent.Type.MouseButtonRelease,
    QtCore.QEvent.Type.MouseButtonDblClick,
    QtCore.QEvent.Type.KeyPress,
    QtCore.QEvent.Type.Shortcut,
    QtCore.QEvent.Type.Drop,
    QtCore.QEvent.Type.ContextMenu,
})


_MIN_SINGLE_SHOT_ARGS = 2


def _is_skipped_slot(slot: Any) -> bool:
    if getattr(slot, "_prettyqt_skip_trace", False):
        return True
    if getattr(slot, "_prettyqt_traced_slot", False):
        return True
    func = getattr(slot, "__func__", None)
    return bool(
        func is not None
        and (
            getattr(func, "_prettyqt_skip_trace", False)
            or getattr(func, "_prettyqt_traced_slot", False)
        )
    )


def traced_slot(
    name: str | None = None,
    *,
    attributes: Mapping[str, Any] | None = None,
    tracer_provider: Any = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator wrapping a sync or `async def` slot in an OpenTelemetry span.

    When `opentelemetry-api` is not installed or no SDK/Logfire provider is
    configured, this executes as a lightweight no-op.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        slot_name = signalhooks.get_callable_name(fn)
        span_name = name or f"qt.slot {slot_name}"
        base_attrs: dict[str, Any] = {"qt.slot.name": slot_name}
        if attributes:
            base_attrs.update(attributes)

        if inspect.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = _otel.get_tracer(tracer_provider)
                with tracer.start_as_current_span(
                    span_name, attributes=base_attrs
                ) as span:
                    try:
                        return await fn(*args, **kwargs)
                    except BaseException as exc:
                        _otel.record_span_exception(span, exc)
                        raise

            async_wrapper._prettyqt_traced_slot = True  # ty: ignore[missing-attribute]
            return async_wrapper

        @functools.wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            tracer = _otel.get_tracer(tracer_provider)
            with tracer.start_as_current_span(span_name, attributes=base_attrs) as span:
                try:
                    return fn(*args, **kwargs)
                except BaseException as exc:
                    _otel.record_span_exception(span, exc)
                    raise

        sync_wrapper._prettyqt_traced_slot = True  # ty: ignore[missing-attribute]
        return sync_wrapper

    return decorator


class TelemetrySignalHook:
    """SignalHook that creates OpenTelemetry spans (and optional metrics) for slots."""

    # Run before AsyncSlotHook (50) so coroutine bodies are traced before scheduling.
    priority: int = 10

    def __init__(
        self,
        *,
        tracer_provider: Any = None,
        meter_provider: Any = None,
        trace_slots: bool = True,
        trace_emits: bool = False,
        record_metrics: bool = False,
        slot_filter: Callable[[signalhooks.SignalInfo, Callable[..., Any]], bool]
        | None = None,
    ) -> None:
        self._tracer_provider = tracer_provider
        self._trace_slots = trace_slots
        self._trace_emits = trace_emits
        self._slot_filter = slot_filter
        self._slot_counter: Any = None
        self._slot_duration: Any = None
        if record_metrics:
            meter = _otel.get_meter(meter_provider)
            if meter is not None:
                self._slot_counter = meter.create_counter(
                    "qt.slot.calls",
                    unit="1",
                    description="Number of Qt slot invocations",
                )
                self._slot_duration = meter.create_histogram(
                    "qt.slot.duration",
                    unit="ms",
                    description="Duration of Qt slot invocations in milliseconds",
                )

    def _get_tracer(self) -> Any:
        return _otel.get_tracer(self._tracer_provider)

    def wrap_slot(
        self,
        signal_info: signalhooks.SignalInfo,
        slot: Callable[..., Any],
    ) -> Callable[..., Any] | None:
        if not self._trace_slots or _is_skipped_slot(slot):
            return None
        if self._slot_filter is not None and not self._slot_filter(signal_info, slot):
            return None

        slot_name = signalhooks.get_callable_name(slot)
        span_name = f"qt.slot {slot_name}"
        attrs: dict[str, Any] = {
            "qt.signal.name": signal_info.name,
            "qt.signal.signature": signal_info.signature,
            "qt.slot.name": slot_name,
        }
        if signal_info.sender_type:
            attrs["qt.signal.sender_type"] = signal_info.sender_type

        metric_attrs = {
            "qt.signal.name": signal_info.name,
            "qt.slot.name": slot_name,
        }
        slot_counter = self._slot_counter
        slot_duration = self._slot_duration

        if inspect.iscoroutinefunction(slot):

            async def async_invoker(
                target: Callable[..., Any], args: tuple[Any, ...]
            ) -> Any:
                tracer = self._get_tracer()
                t0 = time.perf_counter() if slot_duration is not None else 0.0
                if slot_counter is not None:
                    slot_counter.add(1, metric_attrs)
                with tracer.start_as_current_span(span_name, attributes=attrs) as span:
                    try:
                        return await target(*args)
                    except BaseException as exc:
                        _otel.record_span_exception(span, exc)
                        raise
                    finally:
                        if slot_duration is not None:
                            slot_duration.record(
                                (time.perf_counter() - t0) * 1000.0, metric_attrs
                            )

            return signalhooks.make_safe_slot_wrapper(slot, async_invoker)

        def sync_invoker(target: Callable[..., Any], args: tuple[Any, ...]) -> Any:
            tracer = self._get_tracer()
            t0 = time.perf_counter() if slot_duration is not None else 0.0
            if slot_counter is not None:
                slot_counter.add(1, metric_attrs)
            with tracer.start_as_current_span(span_name, attributes=attrs) as span:
                try:
                    return target(*args)
                except BaseException as exc:
                    _otel.record_span_exception(span, exc)
                    raise
                finally:
                    if slot_duration is not None:
                        slot_duration.record(
                            (time.perf_counter() - t0) * 1000.0, metric_attrs
                        )

        return signalhooks.make_safe_slot_wrapper(slot, sync_invoker)

    def on_emit(
        self,
        signal_info: signalhooks.SignalInfo,
        args: tuple[Any, ...],
    ) -> contextlib.AbstractContextManager[Any] | None:
        if not self._trace_emits:
            return None
        attrs: dict[str, Any] = {
            "qt.signal.name": signal_info.name,
            "qt.signal.signature": signal_info.signature,
            "qt.signal.arg_count": len(args),
        }
        if signal_info.sender_type:
            attrs["qt.signal.sender_type"] = signal_info.sender_type
        return self._get_tracer().start_as_current_span(
            f"qt.emit {signal_info.name}",
            attributes=attrs,
        )


def _event_type_name(event_type: QtCore.QEvent.Type) -> str:
    name = getattr(event_type, "name", None)
    return str(name) if name else str(int(event_type))


class QtInstrumentor:
    """OpenTelemetry instrumentor for Qt / PrettyQt applications.

    Automatically sends spans and metrics to whichever OpenTelemetry
    `TracerProvider` / `MeterProvider` is configured (including Logfire via
    `logfire.configure()`, Jaeger, Grafana Tempo, or `InMemorySpanExporter`).

    Can be used via `instrument()` / `uninstrument()`, as a context manager
    (`with QtInstrumentor(): ...`), or via `with app.trace_mode(): ...`.
    """

    def __init__(
        self,
        *,
        tracer_provider: Any = None,
        meter_provider: Any = None,
        trace_slots: bool = True,
        trace_emits: bool = False,
        trace_ui_events: bool = True,
        trace_timers: bool = True,
        trace_workers: bool = True,
        trace_network: bool = True,
        record_metrics: bool = False,
        ui_event_types: Collection[QtCore.QEvent.Type] | None = None,
        slot_filter: Callable[[signalhooks.SignalInfo, Callable[..., Any]], bool]
        | None = None,
    ) -> None:
        self._tracer_provider = tracer_provider
        self._meter_provider = meter_provider
        self._trace_slots = trace_slots
        self._trace_emits = trace_emits
        self._trace_ui_events = trace_ui_events
        self._trace_timers = trace_timers
        self._trace_workers = trace_workers
        self._trace_network = trace_network
        self._record_metrics = record_metrics
        self._ui_event_types: frozenset[QtCore.QEvent.Type] = (
            DEFAULT_UI_EVENT_TYPES
            if ui_event_types is None
            else frozenset(ui_event_types)
        )
        self._slot_filter = slot_filter

        self._instrumented = False
        self._signal_hook: TelemetrySignalHook | None = None
        self._prev_notify_hook: Any = None
        self._orig_single_shot: Any = None
        self._orig_start_callback_timer: Any = None
        self._orig_start_worker: Any = None
        self._orig_network_methods: dict[str, Any] = {}

    @property
    def is_instrumented(self) -> bool:
        return self._instrumented

    def instrument(self) -> Self:
        """Activate instrumentation hooks."""
        _otel.require_opentelemetry()
        if self._instrumented:
            return self
        if self._trace_slots or self._trace_emits:
            self._install_signal_hook()
        if self._trace_ui_events:
            self._install_notify_hook()
        if self._trace_timers:
            self._install_timer_hooks()
        if self._trace_workers:
            self._install_worker_hook()
        if self._trace_network:
            self._install_network_hooks()
        self._instrumented = True
        return self

    def uninstrument(self) -> None:
        """Deactivate and cleanly restore all patched Qt hooks."""
        if not self._instrumented:
            return
        self._uninstall_network_hooks()
        self._uninstall_worker_hook()
        self._uninstall_timer_hooks()
        self._uninstall_notify_hook()
        self._uninstall_signal_hook()
        self._instrumented = False

    def __enter__(self) -> Self:
        return self.instrument()

    def __exit__(self, *exc_info: object) -> None:
        self.uninstrument()

    # --- Signal / Slot hook ---

    def _install_signal_hook(self) -> None:
        hook = TelemetrySignalHook(
            tracer_provider=self._tracer_provider,
            meter_provider=self._meter_provider,
            trace_slots=self._trace_slots,
            trace_emits=self._trace_emits,
            record_metrics=self._record_metrics,
            slot_filter=self._slot_filter,
        )
        signalhooks.get_hook_manager().register(hook)
        self._signal_hook = hook

    def _uninstall_signal_hook(self) -> None:
        if self._signal_hook is not None:
            signalhooks.get_hook_manager().unregister(self._signal_hook)
            self._signal_hook = None

    # --- UI event notify hook ---

    def _install_notify_hook(self) -> None:
        from prettyqt.core.coreapplication import CoreApplicationMixin

        self._prev_notify_hook = CoreApplicationMixin._notify_hook
        CoreApplicationMixin._notify_hook = self._on_notify

    def _uninstall_notify_hook(self) -> None:
        from prettyqt.core.coreapplication import CoreApplicationMixin

        if CoreApplicationMixin._notify_hook == self._on_notify:
            CoreApplicationMixin._notify_hook = self._prev_notify_hook
        self._prev_notify_hook = None

    def _on_notify(
        self,
        receiver: Any,
        event: Any,
        call_next: Callable[[Any, Any], bool],
    ) -> bool:
        if event is None or event.type() not in self._ui_event_types:
            return call_next(receiver, event)
        ev_name = _event_type_name(event.type())
        attrs: dict[str, Any] = {
            "qt.event.type": ev_name,
            "qt.receiver.type": type(receiver).__name__,
        }
        with contextlib.suppress(RuntimeError, AttributeError):
            if obj_name := receiver.objectName():
                attrs["qt.receiver.name"] = obj_name
        tracer = _otel.get_tracer(self._tracer_provider)
        span_name = f"qt.event {ev_name}"
        with tracer.start_as_current_span(span_name, attributes=attrs) as span:
            try:
                return call_next(receiver, event)
            except BaseException as exc:
                _otel.record_span_exception(span, exc)
                raise

    # --- Timer context propagation hooks ---

    def _install_timer_hooks(self) -> None:
        orig_single_shot = QtCore.QTimer.singleShot

        @staticmethod
        def patched_single_shot(*args: Any, **kwargs: Any) -> Any:
            if (
                len(args) >= _MIN_SINGLE_SHOT_ARGS
                and callable(args[-1])
                and signalhooks.is_wrappable_slot(args[-1])
                and not _is_skipped_slot(args[-1])
            ):
                wrapped_cb = _otel.capture_context(args[-1])
                args = (*args[:-1], wrapped_cb)
            return orig_single_shot(*args, **kwargs)

        try:
            QtCore.QTimer.singleShot = patched_single_shot  # ty: ignore[invalid-assignment]
            self._orig_single_shot = orig_single_shot
        except TypeError:
            logger.debug("Binding does not allow patching QTimer.singleShot")

        from prettyqt.core.object import ObjectMixin

        orig_start_cb = ObjectMixin.start_callback_timer

        def patched_start_callback_timer(
            obj_self: Any,
            callback: Callable[..., Any],
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            if callable(callback) and not _is_skipped_slot(callback):
                callback = _otel.capture_context(callback)
            return orig_start_cb(obj_self, callback, *args, **kwargs)

        ObjectMixin.start_callback_timer = patched_start_callback_timer  # ty: ignore[invalid-assignment]
        self._orig_start_callback_timer = orig_start_cb

    def _uninstall_timer_hooks(self) -> None:
        if self._orig_single_shot is not None:
            QtCore.QTimer.singleShot = self._orig_single_shot
            self._orig_single_shot = None
        if self._orig_start_callback_timer is not None:
            from prettyqt.core.object import ObjectMixin

            ObjectMixin.start_callback_timer = self._orig_start_callback_timer
            self._orig_start_callback_timer = None

    # --- ThreadPool worker context propagation & span ---

    def _install_worker_hook(self) -> None:
        from prettyqt.core.threadpool import ThreadPool, Worker

        orig_start_worker = ThreadPool.start_worker
        tracer_provider = self._tracer_provider

        def patched_start_worker(
            pool_self: Any,
            fn_or_worker: Callable[..., Any] | Worker,
            args: tuple[Any, ...] | None = None,
            kwargs: dict[str, Any] | None = None,
            priority: int = 0,
            result_fn: Callable[..., Any] | None = None,
            finished_fn: Callable[..., Any] | None = None,
            progress_fn: Callable[..., Any] | None = None,
            error_fn: Callable[..., Any] | None = None,
        ) -> Any:
            if callable(fn_or_worker):
                worker = Worker(
                    fn_or_worker,
                    *(args or ()),
                    **(kwargs or {}),
                )
            else:
                worker = fn_or_worker

            fn_name = signalhooks.get_callable_name(worker.fn)
            orig_fn = worker.fn
            captured = _otel.get_current_context()

            if inspect.isgeneratorfunction(orig_fn):

                def traced_gen(*w_args: Any, **w_kwargs: Any) -> Any:
                    token = _otel.attach_context(captured)
                    tracer = _otel.get_tracer(tracer_provider)
                    attrs = {
                        "qt.worker.name": fn_name,
                        "thread.name": threading.current_thread().name,
                    }
                    try:
                        with tracer.start_as_current_span(
                            f"qt.worker {fn_name}", attributes=attrs
                        ) as span:
                            try:
                                yield from orig_fn(*w_args, **w_kwargs)
                            except BaseException as exc:
                                _otel.record_span_exception(span, exc)
                                raise
                    finally:
                        _otel.detach_context(token)

                worker.fn = traced_gen
            else:

                def traced_fn(*w_args: Any, **w_kwargs: Any) -> Any:
                    token = _otel.attach_context(captured)
                    tracer = _otel.get_tracer(tracer_provider)
                    attrs = {
                        "qt.worker.name": fn_name,
                        "thread.name": threading.current_thread().name,
                    }
                    try:
                        with tracer.start_as_current_span(
                            f"qt.worker {fn_name}", attributes=attrs
                        ) as span:
                            try:
                                return orig_fn(*w_args, **w_kwargs)
                            except BaseException as exc:
                                _otel.record_span_exception(span, exc)
                                raise
                    finally:
                        _otel.detach_context(token)

                worker.fn = traced_fn

            if result_fn is not None:
                result_fn = _otel.capture_context(result_fn)
            if finished_fn is not None:
                finished_fn = _otel.capture_context(finished_fn)
            if progress_fn is not None:
                progress_fn = _otel.capture_context(progress_fn)
            if error_fn is not None:
                error_fn = _otel.capture_context(error_fn)

            return orig_start_worker(
                pool_self,
                worker,
                priority=priority,
                result_fn=result_fn,
                finished_fn=finished_fn,
                progress_fn=progress_fn,
                error_fn=error_fn,
            )

        ThreadPool.start_worker = patched_start_worker  # ty: ignore[invalid-assignment]
        self._orig_start_worker = orig_start_worker

    def _uninstall_worker_hook(self) -> None:
        if self._orig_start_worker is not None:
            from prettyqt.core.threadpool import ThreadPool

            ThreadPool.start_worker = self._orig_start_worker
            self._orig_start_worker = None

    # --- QNetworkAccessManager W3C traceparent injection & client spans ---

    def _install_network_hooks(self) -> None:
        try:
            from prettyqt.qt import QtNetwork
        except ImportError:
            return

        nam_cls = QtNetwork.QNetworkAccessManager
        tracer_provider = self._tracer_provider
        method_map = {
            "get": "GET",
            "head": "HEAD",
            "post": "POST",
            "put": "PUT",
            "deleteResource": "DELETE",
        }

        for attr, http_method in method_map.items():
            orig_method = getattr(nam_cls, attr, None)
            if orig_method is None:
                continue

            def _make_wrapper(orig: Any, verb: str) -> Callable[..., Any]:
                def wrapped(
                    nam_self: Any,
                    request: Any,
                    *rest: Any,
                    **kwargs: Any,
                ) -> Any:
                    if not isinstance(request, QtNetwork.QNetworkRequest):
                        return orig(nam_self, request, *rest, **kwargs)
                    tracer = _otel.get_tracer(tracer_provider)
                    url_str = request.url().toString()
                    span = tracer.start_span(
                        f"HTTP {verb}",
                        kind=_otel.client_span_kind(),
                        attributes={
                            "http.request.method": verb,
                            "url.full": url_str,
                        },
                    )
                    ctx = _otel.set_span_in_context(span)
                    _otel.inject_trace_headers(request, context=ctx)
                    try:
                        reply = orig(nam_self, request, *rest, **kwargs)
                    except BaseException as exc:
                        _otel.record_span_exception(span, exc)
                        span.end()
                        raise

                    if reply is not None:
                        status_attr = (
                            QtNetwork.QNetworkRequest.Attribute.HttpStatusCodeAttribute
                        )
                        no_err = QtNetwork.QNetworkReply.NetworkError.NoError

                        def _on_finished() -> None:
                            try:
                                code = reply.attribute(status_attr)
                                if code is not None:
                                    span.set_attribute(
                                        "http.response.status_code", int(code)
                                    )
                                err = reply.error()
                                if err != no_err:
                                    _otel.set_span_error(span, reply.errorString())
                            finally:
                                span.end()

                        _on_finished._prettyqt_skip_trace = True  # ty: ignore[missing-attribute]
                        reply.finished.connect(_on_finished)
                    else:
                        span.end()
                    return reply

                return wrapped

            try:
                setattr(nam_cls, attr, _make_wrapper(orig_method, http_method))
                self._orig_network_methods[attr] = orig_method
            except TypeError:
                logger.debug(
                    "Binding does not allow patching QNetworkAccessManager.%s", attr
                )

    def _uninstall_network_hooks(self) -> None:
        if not self._orig_network_methods:
            return
        from prettyqt.qt import QtNetwork

        nam_cls = QtNetwork.QNetworkAccessManager
        for attr, orig_method in self._orig_network_methods.items():
            setattr(nam_cls, attr, orig_method)
        self._orig_network_methods.clear()


class TracingStalker:
    """Observes all signals of a `QObject` and records OTel span events & metrics.

    Useful for diagnosing signal storms or tracing emissions on a specific
    widget/model without globally wrapping slots.
    """

    def __init__(
        self,
        qobject: QtCore.QObject,
        *,
        meter_provider: Any = None,
        record_span_events: bool = True,
        record_metrics: bool = True,
    ) -> None:
        self._obj = qobject
        self._record_span_events = record_span_events
        self._handles: list[tuple[Any, Any]] = []
        self._signal_counter: Any = None
        if record_metrics:
            meter = _otel.get_meter(meter_provider)
            if meter is not None:
                self._signal_counter = meter.create_counter(
                    "qt.signal.emitted",
                    unit="1",
                    description="Number of Qt signals emitted by observed objects",
                )

    def hook(self) -> Self:
        """Connect observer slots to every signal exposed by the target QObject."""
        qmeta = self._obj.metaObject()
        if qmeta is None:
            return self
        meta = core.MetaObject(qmeta)
        obj_type = type(self._obj).__name__
        for signal in meta.get_signals(only_notifiers=False):
            sig_name = signal.get_name()
            if not hasattr(self._obj, sig_name):
                continue
            sig_instance = getattr(self._obj, sig_name)
            cb = self._make_callback(obj_type, sig_name)
            conn = sig_instance.connect(cb)
            self._handles.append((sig_instance, conn))
        return self

    def unhook(self) -> None:
        """Disconnect all observer slots."""
        for sig_instance, conn in self._handles:
            with contextlib.suppress(RuntimeError, TypeError):
                sig_instance.disconnect(conn)
        self._handles.clear()

    def __enter__(self) -> Self:
        return self.hook()

    def __exit__(self, *exc_info: object) -> None:
        self.unhook()

    def _make_callback(self, obj_type: str, sig_name: str) -> Callable[..., None]:
        def _on_signal(*args: Any) -> None:
            attrs: dict[str, Any] = {
                "qt.signal.name": sig_name,
                "qt.sender.type": obj_type,
                "qt.signal.arg_count": len(args),
            }
            if self._record_span_events:
                span = _otel.get_current_span()
                if span is not None and span.is_recording():
                    span.add_event(f"qt.signal.{sig_name}", attributes=attrs)
            if self._signal_counter is not None:
                self._signal_counter.add(
                    1, {"qt.signal.name": sig_name, "qt.sender.type": obj_type}
                )

        _on_signal._prettyqt_skip_trace = True  # ty: ignore[missing-attribute]
        return _on_signal


_global_instrumentor: QtInstrumentor | None = None


def instrument(**kwargs: Any) -> QtInstrumentor:
    """Instrument Qt / PrettyQt globally with OpenTelemetry."""
    global _global_instrumentor
    if _global_instrumentor is not None and _global_instrumentor.is_instrumented:
        _global_instrumentor.uninstrument()
    _global_instrumentor = QtInstrumentor(**kwargs).instrument()
    return _global_instrumentor


def uninstrument() -> None:
    """Uninstrument the global `QtInstrumentor` if active."""
    global _global_instrumentor
    if _global_instrumentor is not None:
        _global_instrumentor.uninstrument()
        _global_instrumentor = None
