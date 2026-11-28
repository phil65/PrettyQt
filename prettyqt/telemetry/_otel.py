"""Optional OpenTelemetry API helpers with safe no-op fallbacks.

Depends only on `opentelemetry-api` (optional extra `prettyqt[telemetry]`).
When an OpenTelemetry SDK or Logfire (`logfire.configure()`) is configured by
the application, spans, metrics, and propagated headers flow there automatically.
When `opentelemetry-api` is not installed, helpers like `traced_slot`,
`capture_context`, and `inject_trace_headers` degrade cleanly to no-ops.
"""

import contextlib
import functools
from typing import TYPE_CHECKING, Any

import prettyqt
from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from prettyqt.qt import QtNetwork


try:
    from opentelemetry import (
        context as otel_context,
        metrics as otel_metrics,
        propagate as otel_propagate,
        trace as otel_trace,
    )
    from opentelemetry.trace import SpanKind, Status, StatusCode

    HAS_OPENTELEMETRY = True
except ImportError:  # pragma: no cover
    otel_context = None  # type: ignore[assignment]
    otel_metrics = None  # type: ignore[assignment]
    otel_propagate = None  # type: ignore[assignment]
    otel_trace = None  # type: ignore[assignment]
    SpanKind = None  # type: ignore[assignment,misc]
    Status = None  # type: ignore[assignment,misc]
    StatusCode = None  # type: ignore[assignment,misc]
    HAS_OPENTELEMETRY = False


class _NoOpSpan:
    def set_attribute(self, key: str, value: Any) -> None:
        pass

    def set_attributes(self, attributes: dict[str, Any]) -> None:
        pass

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        pass

    def record_exception(self, exception: BaseException) -> None:
        pass

    def set_status(self, status: Any, description: str | None = None) -> None:
        pass

    def end(self) -> None:
        pass


class _NoOpTracer:
    @contextlib.contextmanager
    def start_as_current_span(self, *_args: Any, **_kwargs: Any) -> Generator[_NoOpSpan]:
        yield _NoOpSpan()

    def start_span(self, *_args: Any, **_kwargs: Any) -> _NoOpSpan:
        return _NoOpSpan()


_NOOP_TRACER = _NoOpTracer()


def require_opentelemetry() -> None:
    """Raise a helpful `ImportError` if `opentelemetry-api` is unavailable."""
    if not HAS_OPENTELEMETRY:
        msg = (
            "opentelemetry-api is required for QtInstrumentor. "
            "Install it with `pip install opentelemetry-api` or "
            "`pip install prettyqt[telemetry]`."
        )
        raise ImportError(msg)


def get_tracer(
    tracer_provider: Any = None,
    *,
    name: str = "prettyqt",
    version: str | None = None,
) -> Any:
    """Return an OpenTelemetry Tracer (or no-op tracer if OTel is unavailable)."""
    if otel_trace is None:
        return _NOOP_TRACER
    ver = prettyqt.__version__ if version is None else version
    return otel_trace.get_tracer(name, ver, tracer_provider=tracer_provider)


def get_meter(
    meter_provider: Any = None,
    *,
    name: str = "prettyqt",
    version: str | None = None,
) -> Any:
    """Return an OpenTelemetry Meter (or `None` if OTel is unavailable)."""
    if otel_metrics is None:
        return None
    ver = prettyqt.__version__ if version is None else version
    return otel_metrics.get_meter(name, ver, meter_provider=meter_provider)


def get_current_context() -> Any:
    return None if otel_context is None else otel_context.get_current()


def attach_context(ctx: Any) -> Any:
    return None if otel_context is None else otel_context.attach(ctx)


def detach_context(token: Any) -> None:
    if otel_context is not None and token is not None:
        otel_context.detach(token)


def get_current_span() -> Any:
    return None if otel_trace is None else otel_trace.get_current_span()


def set_span_in_context(span: Any) -> Any:
    return None if otel_trace is None else otel_trace.set_span_in_context(span)


def client_span_kind() -> Any:
    return None if SpanKind is None else SpanKind.CLIENT


def set_span_error(span: Any, description: str) -> None:
    if Status is not None and StatusCode is not None:
        span.set_status(Status(StatusCode.ERROR, description))


def record_span_exception(span: Any, exc: BaseException) -> None:
    """Record an exception and mark the span status as ERROR."""
    span.record_exception(exc)
    set_span_error(span, str(exc))


def capture_context[**P, T](fn: Callable[P, T]) -> Callable[P, T]:
    """Wrap `fn` so it executes within the currently active OpenTelemetry context.

    Useful whenever crossing a Qt boundary that does not carry Python
    `contextvars` (such as `QTimer.singleShot`, `QThread`, or `QRunnable`).
    """
    if otel_context is None:
        return fn
    captured = otel_context.get_current()

    @functools.wraps(fn)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        token = attach_context(captured)
        try:
            return fn(*args, **kwargs)
        finally:
            detach_context(token)

    return wrapped


def inject_trace_headers(
    request: QtNetwork.QNetworkRequest,
    *,
    context: Any = None,
) -> QtNetwork.QNetworkRequest:
    """Inject W3C trace headers (`traceparent`, `tracestate`, etc.) into a request."""
    if otel_propagate is None:
        return request
    carrier: dict[str, str] = {}
    otel_propagate.inject(carrier, context=context)
    for key, value in carrier.items():
        request.setRawHeader(
            QtCore.QByteArray(key.encode("utf-8")),
            QtCore.QByteArray(value.encode("utf-8")),
        )
    return request
