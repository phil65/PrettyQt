"""OpenTelemetry observability and instrumentation for PrettyQt.

Requires optional `opentelemetry-api` (`pip install prettyqt[telemetry]`) for
active tracing and metrics, and works automatically with Logfire
(`logfire.configure()`), Jaeger, Grafana Tempo, or any OpenTelemetry SDK
exporter.
"""

from ._otel import (
    HAS_OPENTELEMETRY,
    capture_context,
    get_meter,
    get_tracer,
    inject_trace_headers,
)
from .instrumentor import (
    DEFAULT_UI_EVENT_TYPES,
    QtInstrumentor,
    TelemetrySignalHook,
    TracingStalker,
    instrument,
    traced_slot,
    uninstrument,
)


__all__ = [
    "DEFAULT_UI_EVENT_TYPES",
    "HAS_OPENTELEMETRY",
    "QtInstrumentor",
    "TelemetrySignalHook",
    "TracingStalker",
    "capture_context",
    "get_meter",
    "get_tracer",
    "inject_trace_headers",
    "instrument",
    "traced_slot",
    "uninstrument",
]
