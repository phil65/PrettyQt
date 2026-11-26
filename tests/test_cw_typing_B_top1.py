# ruff: noqa: N999
"""Regression tests for runtime bugs found while fixing ty diagnostics."""

import logging
import typing

from prettyqt import constants, custom_widgets, gui, widgets
from prettyqt.custom_widgets.logtextedit import Message


def test_astviewer_set_ast_syntax_error_on_empty_model(qtbot):
    viewer = custom_widgets.AstViewer()
    qtbot.addWidget(viewer)
    viewer.set_ast("def (:")
    assert viewer.ast_textedit.text() == ""


def test_astviewer_rename_variable_with_none_ast_tree(qtbot):
    viewer = custom_widgets.AstViewer()
    qtbot.addWidget(viewer)
    viewer.set_ast("def (:")
    viewer.rename_variable("a", "b")
    assert viewer.ast_textedit.text() == ""


def test_commandpalette_match_color_getter_and_setter(qtbot):
    palette = custom_widgets.CommandPalette()
    qtbot.addWidget(palette)
    assert palette.match_color() == "#468cc6"
    palette.set_match_color("red")
    assert palette.match_color() == "#ff0000"
    palette.add_actions([gui.Action(text="Open File")])
    palette._table._proxy.set_search_term("op")
    rendered = palette._table._proxy.index(0, 0).data()
    assert "#ff0000" in rendered


def test_crossfadewidget_init_timeline_signal(qtbot):
    w1 = widgets.Label("one")
    w2 = widgets.Label("two")
    qtbot.addWidget(w1)
    qtbot.addWidget(w2)
    widget = custom_widgets.CrossFadeWidget(w1, w2)
    qtbot.addWidget(widget)
    widget.timeline.valueChanged.emit(0.5)
    assert widget.get_blend_factor() == 0.5  # noqa: PLR2004


def test_logtextedit_message_format_string_with_false_exc_info():
    formatter = logging.Formatter("%(message)s")
    highlighter = Message(formatter)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello %s",
        args=("world",),
        exc_info=None,
    )
    record.exc_info = False
    assert highlighter.format_string(record) == "hello world"


def test_multicombobox_toggle_all_uses_standard_item_model_change_layout(qtbot):
    combo = custom_widgets.MultiComboBox()
    qtbot.addWidget(combo)
    toggle_all = combo._model.item(0)
    assert toggle_all is not None
    assert toggle_all.checkState() == constants.CheckState.Checked
    combo.addItems(["a", "b"], all_checked=True)
    assert combo.get_value() == ["a", "b"]
    toggle_all.setCheckState(constants.CheckState.Unchecked)
    assert combo.get_value() == []
    toggle_all.setCheckState(constants.CheckState.Checked)
    assert combo.get_value() == ["a", "b"]


def test_multicombobox_add_items_tuples_and_all_checked(qtbot):
    combo = custom_widgets.MultiComboBox()
    qtbot.addWidget(combo)
    combo.addItems([("One", 1), ("Two", 2)], all_checked=True)
    assert combo.currentData() == [1, 2]
    assert combo.get_current_options() == [("One", 1), ("Two", 2)]


def test_multicombobox_set_value_sets_checkstate(qtbot):
    combo = custom_widgets.MultiComboBox()
    qtbot.addWidget(combo)
    combo.addItems(["a", "b", "c"])
    combo.set_value(["b"])
    assert combo.get_value() == ["b"]
    combo.set_value(["a", "c"])
    assert combo.get_value() == ["a", "c"]


def test_qobjecthierarchytreeview_select_object_keyword_role(qtbot):
    parent = widgets.Widget()
    child = widgets.PushButton("child", parent=parent)
    qtbot.addWidget(parent)
    view = custom_widgets.QObjectHierarchyTreeView()
    qtbot.addWidget(view)
    view.select_object(child)
    view.set_qobject(parent)
    view.select_object(child)


def test_roundprogressbar_paint_event_type_hints():
    hints = typing.get_type_hints(custom_widgets.RoundProgressBar.paintEvent)
    assert hints["event"] is gui.QPaintEvent


def test_roundprogressbar_data_colors_brush(qtbot):
    bar = custom_widgets.RoundProgressBar()
    qtbot.addWidget(bar)
    bar.resize(100, 100)
    bar.set_data_colors([(0.0, "red"), (1.0, "blue")])
    bar.grab()
    brush = bar.palette().brush(
        gui.QPalette.ColorGroup.Active, gui.QPalette.ColorRole.Highlight
    )
    gradient = brush.gradient()
    assert gradient is not None
    assert gradient.type() == gui.QGradient.Type.ConicalGradient


def test_roundprogressbar_expand_style_uses_radial_gradient(qtbot):
    bar = custom_widgets.RoundProgressBar()
    qtbot.addWidget(bar)
    bar.resize(100, 100)
    bar.set_bar_style("expand")
    bar.set_data_colors([(0.0, "red"), (1.0, "blue")])
    bar.grab()
    brush = bar.palette().brush(
        gui.QPalette.ColorGroup.Active, gui.QPalette.ColorRole.Highlight
    )
    gradient = brush.gradient()
    assert gradient is not None
    assert gradient.type() == gui.QGradient.Type.RadialGradient
