"""Tests for OpenTelemetry instrumentation in `prettyqt.telemetry`."""

import asyncio
from typing import Any

import pytest


otel_trace = pytest.importorskip("opentelemetry.trace")
otel_sdk_trace = pytest.importorskip("opentelemetry.sdk.trace")
otel_sdk_export = pytest.importorskip("opentelemetry.sdk.trace.export")
otel_in_memory = pytest.importorskip(
    "opentelemetry.sdk.trace.export.in_memory_span_exporter"
)
otel_sdk_metrics = pytest.importorskip("opentelemetry.sdk.metrics")
otel_sdk_metrics_export = pytest.importorskip("opentelemetry.sdk.metrics.export")

import prettyqt  # noqa: E402
from prettyqt import constants, core, gui, network, telemetry, widgets  # noqa: E402


def _make_provider() -> tuple[Any, Any]:
    exporter = otel_in_memory.InMemorySpanExporter()
    provider = otel_sdk_trace.TracerProvider()
    provider.add_span_processor(otel_sdk_export.SimpleSpanProcessor(exporter))
    return provider, exporter


def test_ui_event_to_slot_chain_hierarchy(qapp):
    provider, exporter = _make_provider()
    btn = widgets.PushButton("Save", object_name="save_btn")
    chained = core.Object()
    seen: list[str] = []

    def on_name_changed(name: str) -> None:
        seen.append(name)

    def on_click() -> None:
        chained.setObjectName("saved")

    with telemetry.QtInstrumentor(tracer_provider=provider):
        btn.clicked.connect(on_click)
        chained.objectNameChanged.connect(on_name_changed)

        # Simulate mouse press + release so QPushButton emits clicked.
        pos = core.QPointF(5, 5)
        press = gui.QMouseEvent(
            core.QEvent.Type.MouseButtonPress,
            pos,
            pos,
            constants.MouseButton.LeftButton,
            constants.MouseButton.LeftButton,
            constants.KeyboardModifier.NoModifier,
        )
        release = gui.QMouseEvent(
            core.QEvent.Type.MouseButtonRelease,
            pos,
            pos,
            constants.MouseButton.LeftButton,
            constants.MouseButton.NoButton,
            constants.KeyboardModifier.NoModifier,
        )
        btn.resize(80, 30)
        widgets.Application.sendEvent(btn, press)
        widgets.Application.sendEvent(btn, release)

    assert seen == ["saved"]
    spans = exporter.get_finished_spans()
    by_name = {s.name: s for s in spans}

    event_span = by_name["qt.event MouseButtonRelease"]
    click_span = next(s for s in spans if "on_click" in s.name)
    chain_span = next(s for s in spans if "on_name_changed" in s.name)

    # Full parent -> child -> grandchild trace lineage!
    assert event_span.attributes["qt.receiver.name"] == "save_btn"
    assert click_span.context.trace_id == event_span.context.trace_id
    assert click_span.parent.span_id == event_span.context.span_id
    assert chain_span.context.trace_id == event_span.context.trace_id
    assert chain_span.parent.span_id == click_span.context.span_id
    assert chain_span.attributes["qt.signal.name"] == "objectNameChanged"


def test_slot_exception_recorded_on_span(qapp, qtbot):
    provider, exporter = _make_provider()
    obj = core.Object()

    def failing_slot(name: str) -> None:
        msg = f"boom:{name}"
        raise ValueError(msg)

    with telemetry.QtInstrumentor(tracer_provider=provider):
        obj.objectNameChanged.connect(failing_slot)
        with qtbot.capture_exceptions() as exceptions:
            obj.setObjectName("bad")

    assert len(exceptions) == 1
    assert isinstance(exceptions[0][1], ValueError)
    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    span = spans[0]
    assert span.status.status_code == otel_trace.StatusCode.ERROR
    assert any(ev.name == "exception" for ev in span.events)


@pytest.mark.parametrize("telemetry_first", [True, False])
def test_telemetry_composes_with_async_slots(qapp, qtbot, telemetry_first: bool):
    provider, exporter = _make_provider()
    tracer = provider.get_tracer("test")
    obj = core.Object()
    done: list[str] = []

    async def on_name_async(name: str) -> None:
        await asyncio.sleep(0.01)
        val = await core.run_in_gui_thread(lambda: f"gui:{name}")
        with tracer.start_as_current_span("after_gui_return"):
            done.append(val)

    inst = telemetry.QtInstrumentor(tracer_provider=provider)
    try:
        if telemetry_first:
            inst.instrument()
            core.enable_async_slots()
        else:
            core.enable_async_slots()
            inst.instrument()

        obj.objectNameChanged.connect(on_name_async)
        with tracer.start_as_current_span("root_action") as root:
            root_trace_id = root.get_span_context().trace_id
            root_span_id = root.get_span_context().span_id
            obj.setObjectName("async-test")

        qtbot.waitUntil(lambda: done == ["gui:async-test"], timeout=3000)
        # Wait briefly for span exit after list append.
        qtbot.waitUntil(
            lambda: any("on_name_async" in s.name for s in exporter.get_finished_spans()),
            timeout=3000,
        )
    finally:
        core.disable_async_slots()
        inst.uninstrument()
        core.aio.stop_async_bridge()

    spans = exporter.get_finished_spans()
    slot_span = next(s for s in spans if "on_name_async" in s.name)
    inner_span = next(s for s in spans if s.name == "after_gui_return")

    assert slot_span.context.trace_id == root_trace_id
    assert slot_span.parent.span_id == root_span_id
    assert inner_span.context.trace_id == root_trace_id
    assert inner_span.parent.span_id == slot_span.context.span_id


def test_traced_slot_decorator_and_no_double_wrap(qapp):
    provider, exporter = _make_provider()
    obj = core.Object()
    called: list[str] = []

    @telemetry.traced_slot("custom.slot", tracer_provider=provider)
    def handle(name: str) -> None:
        called.append(name)

    with telemetry.QtInstrumentor(tracer_provider=provider):
        obj.objectNameChanged.connect(handle)
        obj.setObjectName("once")

    assert called == ["once"]
    spans = exporter.get_finished_spans()
    assert [s.name for s in spans] == ["custom.slot"]


def test_timer_context_propagation(qapp, qtbot):
    provider, exporter = _make_provider()
    tracer = provider.get_tracer("test")
    obj = core.Object()
    fired: list[str] = []

    def from_single_shot() -> None:
        with tracer.start_as_current_span("in_single_shot"):
            fired.append("single")

    def from_cb_timer() -> None:
        with tracer.start_as_current_span("in_cb_timer"):
            fired.append("cb")

    with telemetry.QtInstrumentor(tracer_provider=provider):
        with tracer.start_as_current_span("schedule_timers") as root:
            root_trace_id = root.get_span_context().trace_id
            root_span_id = root.get_span_context().span_id
            core.QTimer.singleShot(5, from_single_shot)
            obj.start_callback_timer(from_cb_timer, 5, single_shot=True)

        qtbot.waitUntil(lambda: set(fired) == {"single", "cb"}, timeout=3000)

    spans = {s.name: s for s in exporter.get_finished_spans()}
    for child_name in ("in_single_shot", "in_cb_timer"):
        child = spans[child_name]
        assert child.context.trace_id == root_trace_id
        assert child.parent.span_id == root_span_id


def test_threadpool_worker_context_propagation(qapp, qtbot):
    provider, exporter = _make_provider()
    tracer = provider.get_tracer("test")
    pool = core.ThreadPool()
    results: list[int] = []

    def compute(x: int) -> int:
        with tracer.start_as_current_span("inside_worker"):
            return x + 1

    def on_result(val: int) -> None:
        with tracer.start_as_current_span("on_worker_result"):
            results.append(val)

    with telemetry.QtInstrumentor(tracer_provider=provider):
        with tracer.start_as_current_span("kickoff") as root:
            root_trace_id = root.get_span_context().trace_id
            root_span_id = root.get_span_context().span_id
            pool.start_worker(compute, args=(41,), result_fn=on_result)

        qtbot.waitUntil(lambda: results == [42], timeout=3000)
        pool.waitForDone(3000)

    spans = exporter.get_finished_spans()
    worker_span = next(s for s in spans if "qt.worker" in s.name)
    inside_span = next(s for s in spans if s.name == "inside_worker")
    result_span = next(s for s in spans if s.name == "on_worker_result")

    assert worker_span.context.trace_id == root_trace_id
    assert worker_span.parent.span_id == root_span_id
    assert inside_span.parent.span_id == worker_span.context.span_id
    assert result_span.context.trace_id == root_trace_id


def test_network_request_traceparent_injection(qapp):
    provider, _exporter = _make_provider()
    tracer = provider.get_tracer("test")

    req = network.NetworkRequest(core.Url("https://example.com/api"))
    with tracer.start_as_current_span("outbound") as span:
        telemetry.inject_trace_headers(req)
        expected_trace = f"{span.get_span_context().trace_id:032x}"
        expected_span = f"{span.get_span_context().span_id:016x}"

    header_name = b"traceparent" if prettyqt.qt.PYQT6 else "traceparent"
    raw = bytes(req.rawHeader(header_name)).decode()  # type: ignore[arg-type]
    assert raw.startswith(f"00-{expected_trace}-{expected_span}-")


def test_slot_filter_trace_emits_and_metrics(qapp):
    provider, exporter = _make_provider()
    metric_reader = otel_sdk_metrics_export.InMemoryMetricReader()
    meter_provider = otel_sdk_metrics.MeterProvider(metric_readers=[metric_reader])
    obj = core.Object()

    def allowed(name: str) -> None:
        pass

    def ignored(name: str) -> None:
        pass

    with telemetry.QtInstrumentor(
        tracer_provider=provider,
        meter_provider=meter_provider,
        trace_emits=True,
        record_metrics=True,
        slot_filter=lambda _info, slot: getattr(slot, "__name__", "") != "ignored",
    ):
        obj.objectNameChanged.connect(allowed)
        obj.objectNameChanged.connect(ignored)
        obj.objectNameChanged.emit("hello")

    spans = exporter.get_finished_spans()
    names = [s.name for s in spans]
    assert any(n == "qt.emit objectNameChanged" for n in names)
    assert any("allowed" in n for n in names)
    assert not any("ignored" in n for n in names)

    metrics_data = metric_reader.get_metrics_data()
    metric_names = {
        m.name
        for rm in metrics_data.resource_metrics
        for sm in rm.scope_metrics
        for m in sm.metrics
    }
    assert "qt.slot.calls" in metric_names
    assert "qt.slot.duration" in metric_names


def test_tracing_stalker_and_app_trace_mode(qapp):
    provider, exporter = _make_provider()
    metric_reader = otel_sdk_metrics_export.InMemoryMetricReader()
    meter_provider = otel_sdk_metrics.MeterProvider(metric_readers=[metric_reader])
    tracer = provider.get_tracer("test")
    obj = core.Object()

    with qapp.trace_mode(tracer_provider=provider) as inst:
        assert inst.is_instrumented
        with (
            telemetry.TracingStalker(obj, meter_provider=meter_provider),
            tracer.start_as_current_span("stalk_scope"),
        ):
            obj.setObjectName("watched")
    assert not inst.is_instrumented

    spans = exporter.get_finished_spans()
    stalk_span = next(s for s in spans if s.name == "stalk_scope")
    assert any(ev.name == "qt.signal.objectNameChanged" for ev in stalk_span.events)

    metrics_data = metric_reader.get_metrics_data()
    metric_names = {
        m.name
        for rm in metrics_data.resource_metrics
        for sm in rm.scope_metrics
        for m in sm.metrics
    }
    assert "qt.signal.emitted" in metric_names
