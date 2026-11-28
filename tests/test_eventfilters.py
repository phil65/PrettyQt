"""Tests for `prettyqt.eventfilters`."""

import pytest

from prettyqt import core, eventfilters, gui, widgets


class _RecordingFilter(eventfilters.BaseEventFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events: list[core.QEvent.Type] = []

    def eventFilter(self, obj, event):
        self.events.append(event.type())
        return super().eventFilter(obj, event)


class _CountingTextUpdateFilter(eventfilters.TextUpdateEventFilter):
    def __init__(self, parent, interval: int = 10_000):
        self.update_count = 0
        super().__init__(parent, interval=interval)

    def _update_text(self):
        self.update_count += 1


def test_base_event_filter_applied_to_normal_exit(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    ef = _RecordingFilter()
    assert ef.objectName() == "_RecordingFilter"

    with ef.applied_to(widget) as target:
        assert target is widget
        widgets.Application.sendEvent(widget, core.QEvent(core.QEvent.Type.User))

    count_inside = ef.events.count(core.QEvent.Type.User)
    assert count_inside == 1

    widgets.Application.sendEvent(widget, core.QEvent(core.QEvent.Type.User))
    assert ef.events.count(core.QEvent.Type.User) == count_inside


def test_base_event_filter_applied_to_exception_cleanup(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    ef = _RecordingFilter()

    def _trigger_error():
        with ef.applied_to(widget):
            widgets.Application.sendEvent(widget, core.QEvent(core.QEvent.Type.User))
            msg = "boom"
            raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="boom"):
        _trigger_error()

    count_after_exc = ef.events.count(core.QEvent.Type.User)
    assert count_after_exc == 1

    widgets.Application.sendEvent(widget, core.QEvent(core.QEvent.Type.User))
    assert ef.events.count(core.QEvent.Type.User) == count_after_exc


def test_autosize_columns_event_filter_without_model(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    ef = eventfilters.AutoSizeColumnsEventFilter(view)
    view.installEventFilter(ef)
    assert view.model() is None

    # Should not raise when model is None
    ef._on_scroll()
    resize_event = gui.QResizeEvent(core.QSize(400, 200), core.QSize(100, 100))
    assert ef.eventFilter(view, resize_event) is False
    assert ef._autosized_sections == set()


def test_autosize_columns_event_filter_with_model(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    model = gui.StandardItemModel(2, 3, view)
    for r in range(2):
        for c in range(3):
            model.setItem(r, c, gui.StandardItem(f"cell-{r}-{c}"))
    view.set_model(model)
    view.resize(400, 200)

    ef = eventfilters.AutoSizeColumnsEventFilter(view, orientation="vertical")
    view.installEventFilter(ef)

    resize_event = gui.QResizeEvent(core.QSize(400, 200), core.QSize(100, 100))
    assert ef.eventFilter(view, resize_event) is False
    assert len(ef._autosized_sections) > 0

    # Changing model clears cached autosized sections
    view.set_model(gui.StandardItemModel(1, 1, view))
    assert ef._autosized_sections == set()


def test_autosize_columns_event_filter_horizontal(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    model = gui.StandardItemModel(3, 2, view)
    view.set_model(model)
    view.resize(300, 200)

    ef = eventfilters.AutoSizeColumnsEventFilter(view, orientation="horizontal")
    ef._on_scroll()
    assert len(ef._autosized_sections) > 0


def test_text_update_event_filter_ignores_unrelated_timers(qtbot):
    label = widgets.Label()
    qtbot.addWidget(label)
    ef = _CountingTextUpdateFilter(label, interval=60_000)
    try:
        assert ef.update_count == 1  # initial update in __init__

        unrelated_id = ef._timer_id + 999
        unrelated_event = core.QTimerEvent(unrelated_id)
        assert ef.eventFilter(label, unrelated_event) is False
        assert ef.update_count == 1

        own_event = core.QTimerEvent(ef._timer_id)
        assert ef.eventFilter(label, own_event) is True
        assert ef.update_count == 2  # noqa: PLR2004
    finally:
        label.killTimer(ef._timer_id)


def test_time_and_date_label_event_filters(qtbot):
    time_label = widgets.Label()
    qtbot.addWidget(time_label)
    time_ef = eventfilters.TimeLabelEventFilter(time_label, interval=60_000)
    try:
        assert len(time_label.text()) > 0
    finally:
        time_label.killTimer(time_ef._timer_id)

    date_label = widgets.Label()
    qtbot.addWidget(date_label)
    date_ef = eventfilters.DateLabelEventFilter(date_label, interval=60_000)
    try:
        assert len(date_label.text()) > 0
    finally:
        date_label.killTimer(date_ef._timer_id)


def test_listview_grid_resize_event_filter_clamping(qtbot):
    view = widgets.ListView()
    qtbot.addWidget(view)
    ef = eventfilters.ListViewGridResizeEventFilter(num_columns=5, parent=view)
    view.installEventFilter(ef)

    # Normal width
    view.resize(280, 200)
    ef._resize(view)
    assert view.gridSize() == core.QSize(50, 50)
    assert view.iconSize() == core.QSize(40, 40)

    # Small width (< 30) must clamp to >= 1
    view.resize(10, 10)
    ef._resize(view)
    assert view.gridSize() == core.QSize(1, 1)
    assert view.iconSize() == core.QSize(1, 1)


def test_section_auto_span_event_filter_without_model(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    assert view.model() is None

    ef = eventfilters.SectionAutoSpanEventFilter(view)
    ef._update_spans()
    resize_event = gui.QResizeEvent(core.QSize(300, 200), core.QSize(100, 100))
    assert ef.eventFilter(view, resize_event) is False
