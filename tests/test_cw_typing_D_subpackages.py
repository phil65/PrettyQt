# ruff: noqa: N999
"""Regression tests for runtime bugs found while type-checking custom_widgets."""

import pytest

from prettyqt import constants, core, custom_widgets, gui, widgets


@pytest.mark.parametrize("orientation", [constants.VERTICAL, constants.HORIZONTAL])
def test_annotatedscrollbar_paint_float_rects(qtbot, orientation):
    scrollbar = custom_widgets.AnnotatedScrollBar(orientation)
    qtbot.addWidget(scrollbar)
    scrollbar.set_annotations([(10, 20), (50, 60), (82, 85)])
    scrollbar.resize(20, 200)
    pixmap = scrollbar.grab()
    assert not pixmap.isNull()


def test_previewscrollbar_paint_without_parent(qtbot):
    scrollbar = custom_widgets.PreviewScrollBar()
    qtbot.addWidget(scrollbar)
    scrollbar.resize(150, 200)
    pixmap = scrollbar.grab()
    assert not pixmap.isNull()


def test_smoothscrollbar_init_and_eventfilter_without_parent(qtbot):
    scrollbar = custom_widgets.SmoothScrollBar(trigger=True)
    qtbot.addWidget(scrollbar)
    event = core.QEvent(core.Event.Type.Wheel)
    assert scrollbar.eventFilter(scrollbar, event) is False


def test_smoothscrollbar_with_raw_qabstractscrollarea(qtbot):
    area = widgets.QScrollArea()
    qtbot.addWidget(area)
    area.verticalScrollBar().setRange(0, 1000)
    scrollbar = custom_widgets.SmoothScrollBar(parent=area, trigger=True)
    qtbot.addWidget(scrollbar)
    wheel_delta = 120
    wheel_event = gui.QWheelEvent(
        core.QPointF(10, 10),
        core.QPointF(10, 10),
        core.QPoint(0, 0),
        core.QPoint(0, -wheel_delta),
        constants.MouseButton.NoButton,
        constants.KeyboardModifier.NoModifier,
        constants.ScrollPhase.NoScrollPhase,
        False,
    )
    assert scrollbar.eventFilter(area.viewport(), wheel_event) is True
    assert area.verticalScrollBar().value() == wheel_delta


def test_multilinelayout_grid_sublayout_add_widget_layout_item(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    layout = custom_widgets.MultiLineLayout(parent=widget, row_number=2)
    layout.set_sub_layout_type("grid")
    btn = widgets.PushButton("a")
    sub = widgets.HBoxLayout()
    spacer = widgets.QSpacerItem(10, 10)
    layout.addWidget(btn)
    layout.addLayout(sub)
    layout.addItem(spacer)
    expected_count = 3
    assert layout.count() == expected_count


def test_multilinelayout_take_at_returns_removed_item_and_handles_empty_sublayout(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    layout = custom_widgets.MultiLineLayout(parent=widget, row_number=3)
    buttons = [widgets.PushButton(str(i)) for i in range(4)]
    for btn in buttons:
        layout.addWidget(btn)

    taken_2 = layout.takeAt(2)
    assert taken_2 is not None
    assert taken_2.widget() is buttons[2]
    assert len(layout.layouts) == 1

    taken_0 = layout.takeAt(0)
    assert taken_0 is not None
    assert taken_0.widget() is buttons[0]

    assert layout.takeAt(99) is None


def test_filterheader_create_editors_without_model_or_parent(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    model = gui.StandardItemModel.from_dict(dict(a=["x", "y"], b=[1, 2]))
    view.set_model(model)
    header = custom_widgets.FilterHeader(parent=view)
    view.setHorizontalHeader(header)

    view.set_model(None)
    assert header._editors == []

    header.setParent(None)
    header.create_editors()
    assert header._editors == []
