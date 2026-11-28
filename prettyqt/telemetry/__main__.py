"""Interactive demo sending PrettyQt OpenTelemetry traces to Aspire / OTLP / console.

Run Aspire Dashboard in another terminal (`uv run duty aspire`), then run:

    uv run python -m prettyqt.telemetry
    uv run python -m prettyqt.telemetry --console
"""

import argparse
import asyncio
import time
from typing import Any

from prettyqt import core, widgets


def _configure_sdk(endpoint: str, *, console: bool) -> Any:
    from opentelemetry import metrics, trace
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
        SimpleSpanProcessor,
    )

    resource = Resource.create({"service.name": "prettyqt-demo"})
    provider = TracerProvider(resource=resource)
    if console:
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    else:
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
            OTLPMetricExporter,
        )
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
        )
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics"),
            export_interval_millis=3000,
        )
        metrics.set_meter_provider(
            MeterProvider(resource=resource, metric_readers=[metric_reader])
        )
    trace.set_tracer_provider(provider)
    return provider


def main() -> int:
    from opentelemetry import trace

    parser = argparse.ArgumentParser(description="PrettyQt OpenTelemetry demo")
    parser.add_argument(
        "--endpoint",
        default="http://localhost:4318",
        help="OTLP HTTP base URL (default: http://localhost:4318)",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Print spans to stdout instead of exporting over OTLP HTTP",
    )
    args = parser.parse_args()
    provider = _configure_sdk(args.endpoint, console=args.console)
    tracer = trace.get_tracer("prettyqt.demo")

    app = widgets.app()
    pool = core.ThreadPool()
    chained = core.Object(object_name="chained_target")

    window = widgets.Widget(window_title="PrettyQt OpenTelemetry Demo")
    layout = window.set_layout("vertical")
    status = widgets.Label(
        "Click a button, then inspect traces at http://localhost:18888"
    )
    layout.add(status)

    with app.trace_mode(record_metrics=True), core.async_slots_enabled():
        # 1. Sync signal chain
        def on_chained(name: str) -> None:
            time.sleep(0.02)
            status.setText(f"Chained signal fired: {name}")

        def on_sync_click() -> None:
            time.sleep(0.01)
            chained.setObjectName("updated-from-click")

        chained.objectNameChanged.connect(on_chained)
        sync_btn = widgets.PushButton("1. Sync Signal Chain", object_name="sync_btn")
        sync_btn.clicked.connect(on_sync_click)
        layout.add(sync_btn)

        # 2. Async slot via AsyncBridge
        async def on_async_click() -> None:
            with tracer.start_as_current_span("async_io_step"):
                await asyncio.sleep(0.1)
            await core.run_in_gui_thread(status.setText, "Async slot finished!")

        async_btn = widgets.PushButton("2. Async Slot", object_name="async_btn")
        async_btn.clicked.connect(on_async_click)
        layout.add(async_btn)

        # 3. ThreadPool worker
        def heavy_work() -> str:
            time.sleep(0.12)
            return "Worker finished!"

        def on_worker_click() -> None:
            pool.start_worker(heavy_work, result_fn=status.setText)

        worker_btn = widgets.PushButton("3. Worker Thread", object_name="worker_btn")
        worker_btn.clicked.connect(on_worker_click)
        layout.add(worker_btn)

        # 4. Single-shot timer
        def on_timer_click() -> None:
            def later() -> None:
                with tracer.start_as_current_span("timer_callback"):
                    status.setText("Timer fired inside original trace!")

            core.QTimer.singleShot(80, later)

        timer_btn = widgets.PushButton("4. Delayed Timer", object_name="timer_btn")
        timer_btn.clicked.connect(on_timer_click)
        layout.add(timer_btn)

        # 5. Error span
        def on_error_click() -> None:
            msg = "Intentional demo error"
            raise RuntimeError(msg)

        error_btn = widgets.PushButton("5. Trigger Error Span", object_name="error_btn")
        error_btn.clicked.connect(on_error_click)
        layout.add(error_btn)

        window.resize(360, 220)
        window.show()
        try:
            return app.exec()
        finally:
            provider.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
