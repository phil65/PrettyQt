"""Tests for `prettyqt` package."""

import datetime
import inspect
import os
import pathlib
import pickle
import sys

# import logging
import tempfile

import pytest

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


clsmembers = inspect.getmembers(widgets, inspect.isclass)
clsmembers = [tpl for tpl in clsmembers if not tpl[0].startswith("Abstract")]
clsmembers = [tpl for tpl in clsmembers if QtCore.QObject in tpl[1].mro()]

# logger = logging.getLogger(__name__)


@pytest.mark.parametrize("name, cls", clsmembers)
def test_pickle(name, cls):
    try:
        widget = cls()
    except Exception:
        return None
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


@pytest.mark.parametrize("name, cls", clsmembers)
def test_repr(name, cls):
    try:
        widget = cls()
    except Exception:
        return None
    else:
        repr(widget)


def test_action(qtbot):
    action = widgets.Action()
    action.set_tooltip("test")
    action.set_enabled()
    action.set_disabled()
    action.set_icon(None)
    action.set_icon("mdi.timer")
    action.set_shortcut("Ctrl+A")
    assert action.shortcut().toString() == "Ctrl+A"
    assert action.toolTip() == "test"
    action.set_priority("low")
    with pytest.raises(InvalidParamError):
        action.set_priority("test")
    assert action.get_priority() == "low"
    action.set_menu_role("preferences")
    with pytest.raises(InvalidParamError):
        action.set_menu_role("test")
    assert action.get_menu_role() == "preferences"
    action.set_shortcut_context("widget_with_children")
    with pytest.raises(InvalidParamError):
        action.set_shortcut_context("test")
    assert action.get_shortcut_context() == "widget_with_children"
    action.show_shortcut_in_contextmenu()
    action.set_menu(widgets.Menu())


def test_actiongroup(qtbot):
    group = widgets.ActionGroup(None)
    group.set_exclusion_policy(None)
    group.set_exclusion_policy("exclusive")
    with pytest.raises(InvalidParamError):
        group.set_exclusion_policy("test")
    assert group.get_exclusion_policy() == "exclusive"
    act = widgets.Action()
    group.addAction(act)
    assert group[0] == act
    assert act in group
    assert len(group) == 1


def test_boxlayout(qtbot):
    layout = widgets.BoxLayout("horizontal", margin=0)
    widget = widgets.RadioButton("test")
    layout += widget
    layout2 = widgets.BoxLayout("horizontal")
    layout += layout2
    assert layout[1] == layout2
    layout.set_size_mode("maximum")
    assert layout.get_size_mode() == "maximum"
    layout.set_alignment("left")
    layout.set_alignment("left", widget)
    with pytest.raises(InvalidParamError):
        layout.set_alignment("test")
    # assert layout.get_alignment() == "left"
    with pytest.raises(InvalidParamError):
        layout.set_size_mode("bla")
    layout.set_margin(0)
    assert len(layout) == 2
    layout.add_stretch(1)
    layout.add_spacing(1)
    layout.set_direction("bottom_to_top")
    with pytest.raises(InvalidParamError):
        layout.set_direction("test")
    assert layout.get_direction() == "bottom_to_top"


def test_buttongroup(qtbot):
    widget = widgets.ButtonGroup()
    btn = widgets.RadioButton("test")
    widget.addButton(btn, id=2)
    assert widget[2] == btn


def test_calendarwiget(qtbot):
    widget = widgets.CalendarWidget()
    qtbot.addWidget(widget)
    assert widget.get_date() == widget.get_value()
    widget.set_range(datetime.date(2000, 1, 1), datetime.date(2020, 1, 1))
    widget.set_value(datetime.date(2000, 10, 10))
    widget.set_selection_mode(None)
    widget.set_selection_mode("single")
    assert widget.get_selection_mode() == "single"
    with pytest.raises(InvalidParamError):
        widget.set_selection_mode("test")


def test_checkbox(qtbot):
    widget = widgets.CheckBox()
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    assert bool(widget) is False
    widget.set_value(True)
    assert widget.get_value() is True
    with pytest.raises(InvalidParamError):
        widget.set_checkstate("test")
    widget.is_on = False
    assert widget.is_on is False


def test_colordialog(qtbot):
    dlg = widgets.ColorDialog()
    qtbot.addWidget(dlg)
    assert str(dlg.current_color()) == str(gui.Color("white"))


def test_combobox(qtbot):
    box = widgets.ComboBox()
    qtbot.addWidget(box)
    box.set_disabled()
    box.set_enabled()
    box.add("test", data="data", icon="mdi.timer")
    assert len(box) == 1
    box.set_insert_policy("bottom")
    assert box.get_insert_policy() == "bottom"
    with pytest.raises(InvalidParamError):
        box.set_insert_policy("bla")
    box.set_size_adjust_policy("first_show")
    with pytest.raises(InvalidParamError):
        box.set_size_adjust_policy("bla")
    assert box.get_size_adjust_policy() == "first_show"
    box.set_icon_size(10)
    assert box.get_icon_size() == core.Size(10, 10)
    box.set_min_char_length(10)
    box.add("test2", data="data", icon="mdi.timer")
    box.set_text("test2")
    assert box.text() == "test2"
    box.add_items(dict(a="b"))
    box.add_items(["a"])
    box.add_items([("a", "x")])
    box.get_value()
    box.set_value("x")


def test_commandlinkbutton(qtbot):
    widget = widgets.CommandLinkButton("Test")
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    widget.set_icon("mdi.timer")
    with pytest.raises(InvalidParamError):
        widget.set_style_icon("bla")


def test_completer(qtbot):
    completer = widgets.Completer()
    completer.set_sort_mode(None)
    completer.set_sort_mode("unsorted")
    with pytest.raises(InvalidParamError):
        completer.set_sort_mode("test")
    assert completer.get_sort_mode() == "unsorted"
    completer.set_completion_mode("popup")
    with pytest.raises(InvalidParamError):
        completer.set_completion_mode("test")
    assert completer.get_completion_mode() == "popup"
    completer.set_filter_mode("contains")
    with pytest.raises(InvalidParamError):
        completer.set_filter_mode("test")
    assert completer.get_filter_mode() == "contains"


def test_dateedit(qtbot):
    widget = widgets.DateEdit()
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.date(2000, 11, 11)
    widget.set_value(dt)
    assert widget.get_value() == dt


def test_datetimeedit(qtbot):
    widget = widgets.DateTimeEdit()
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.datetime(2000, 11, 11)
    widget.set_value(dt)
    widget.set_format("dd.MM.yyyy")
    # assert widget.get_value() == dt
    assert widget.get_section_text("day") == "11"
    with pytest.raises(InvalidParamError):
        widget.get_section_text("test")
    widget.set_current_section("day")
    with pytest.raises(InvalidParamError):
        widget.set_current_section("test")
    assert widget.get_current_section() == "day"
    widget.get_displayed_sections()


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_dialog(qtbot, qttester):
    dlg = widgets.Dialog(layout="horizontal")
    qtbot.add_widget(dlg)
    dlg.show()
    qttester.send_keypress(dlg, QtCore.Qt.Key.Key_F11)
    dlg.delete_on_close()
    btn = widgets.RadioButton("test")
    qtbot.addWidget(btn)
    dlg.add_widget(btn)
    dlg.set_icon("mdi.timer")
    dlg.resize(200, 400)
    dlg.resize((150, 400))
    dlg.add_buttonbox()


def test_dial(qtbot):
    widget = widgets.Dial()
    qtbot.addWidget(widget)


def test_dialogbuttonbox(qtbot):
    box = widgets.DialogButtonBox()
    qtbot.addWidget(box)
    box.set_horizontal()
    box.set_vertical()
    btn = box.add_default_button("apply")
    with pytest.raises(InvalidParamError):
        btn = box.add_default_button("test")
    box.set_orientation("horizontal")
    with pytest.raises(InvalidParamError):
        box.set_orientation("test")
    assert box.get_orientation() == "horizontal"
    box.add_button("test_dialogbuttonbox", callback=print)
    assert len(box) == 2
    assert btn == box["apply"]
    assert "apply" in box
    for item in box:
        pass
    btn = box.add_default_buttons(["ok"])


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_dockwidget(qtbot):
    widget = widgets.DockWidget()
    qtbot.addWidget(widget)
    widget.setup_title_bar()
    widget.maximize()
    w = widgets.Widget()
    qtbot.addWidget(w)
    widget.set_widget(w)
    w.raise_dock()


def test_doublespinbox(qtbot):
    widget = widgets.DoubleSpinBox(default_value=5)
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()


def test_filedialog(qtbot):
    dlg = widgets.FileDialog(path_id="test", extension_filter=dict(test=["*.test"]))
    qtbot.addWidget(dlg)
    dlg.set_label_text("accept", "test_filedialog")
    dlg.set_accept_mode("open")
    with pytest.raises(InvalidParamError):
        dlg.set_accept_mode("bla")
    dlg.set_view_mode("detail")
    with pytest.raises(InvalidParamError):
        dlg.set_view_mode("bla")
    dlg.set_label_text("filetype", "test")
    with pytest.raises(InvalidParamError):
        dlg.set_label_text("bla", "test")
    dlg.set_accept_mode("save")
    dlg.set_extension_filter(dict(a=[".csv"]))
    dlg.set_filter("all_dirs")
    with pytest.raises(InvalidParamError):
        dlg.set_filter("test")
    dlg.selected_file()
    dlg.selected_files()
    path = dlg.get_directory()
    dlg.set_directory(path)


def test_filesystemmodel(qttester):
    model = widgets.FileSystemModel()
    model.set_root_path("/")
    idx = model.index(0, 0)
    model.get_paths([idx])
    model.data(idx, model.DATA_ROLE)
    model.yield_child_indexes(idx)
    model.watch_for_changes(False)
    model.use_custom_icons(False)
    model.resolve_sym_links(False)
    model.set_name_filters(["test"], hide=True)
    model.set_filter("drives")
    with pytest.raises(InvalidParamError):
        model.set_filter("test")
    # modeltest.ModelTest(model)
    # qttester.test_model(model, force_py=True)


def test_fontcombobox(qtbot):
    widget = widgets.FontComboBox()
    qtbot.addWidget(widget)
    font = widget.get_current_font()
    assert font == widget.get_value()
    widget.set_font_filters("scalable")
    assert widget.get_font_filters() == ["scalable"]
    with pytest.raises(InvalidParamError):
        widget.set_font_filters("test")


def test_fontdialog(qtbot):
    dlg = widgets.FontDialog()
    qtbot.addWidget(dlg)
    dlg.get_current_font()


def test_formlayout(qtbot):
    layout = widgets.FormLayout()
    layout.set_size_mode("maximum")
    with pytest.raises(InvalidParamError):
        layout.set_size_mode("bla")
    layout[0, "left"] = "0, left"
    button_1 = widgets.RadioButton("1, left")
    qtbot.addWidget(button_1)
    layout[1, "left"] = button_1
    layout[0, "right"] = "label 1 right"
    button_2 = widgets.RadioButton("1, right")
    qtbot.addWidget(button_2)
    layout[1, "right"] = button_2
    layout[2] = "by str"
    button_3 = widgets.RadioButton("widget[3]")
    qtbot.addWidget(button_3)
    layout[3] = button_3
    button_4 = widgets.RadioButton("added with +=")
    qtbot.addWidget(button_4)
    layout += button_4
    button_5 = widgets.RadioButton("tuple")
    qtbot.addWidget(button_5)
    layout += ("added with +=", button_5)
    assert len(layout) == 6
    del layout[0]
    assert isinstance(layout.get_item_position(0), tuple)
    layout.set_row_wrap_policy("wrap_long")
    assert layout.get_row_wrap_policy() == "wrap_long"
    with pytest.raises(InvalidParamError):
        layout.set_row_wrap_policy("test")
    layout.set_field_growth_policy("expanding_fields_grow")
    assert layout.get_field_growth_policy() == "expanding_fields_grow"
    with pytest.raises(InvalidParamError):
        layout.set_field_growth_policy("test")


def test_frame(qtbot):
    frame = widgets.Frame()
    frame.set_frame_shadow("raised")
    assert frame.get_frame_shadow() == "raised"
    with pytest.raises(InvalidParamError):
        frame.set_frame_shadow("test")
    frame.set_frame_shape("panel")
    assert frame.get_frame_shape() == "panel"
    with pytest.raises(InvalidParamError):
        frame.set_frame_shape("test")


def test_gesture():
    gesture = widgets.Gesture()
    assert gesture.get_state() == "none"
    assert gesture.get_gesture_type() == "custom"
    gesture.get_hot_spot()
    gesture.set_gesture_cancel_policy("all_in_context")
    with pytest.raises(InvalidParamError):
        gesture.set_gesture_cancel_policy("test")
    assert gesture.get_gesture_cancel_policy() == "all_in_context"


def test_graphicsblureffect():
    effect = widgets.GraphicsBlurEffect()
    effect.set_blur_hints("animation")
    assert effect.get_blur_hints() == ["animation"]


def test_graphicsitem(qtbot):
    item = widgets.GraphicsItem()
    item.set_panel_modality("scene")
    assert item.get_panel_modality() == "scene"
    with pytest.raises(InvalidParamError):
        item.set_panel_modality("test")
    item.set_cache_mode("item_coordinate")
    assert item.get_cache_mode() == "item_coordinate"
    with pytest.raises(InvalidParamError):
        item.set_cache_mode("test")
    item.set_focus("active_window")
    with pytest.raises(InvalidParamError):
        item.set_focus("test")
    item[0] = "test"
    assert item[0] == "test"
    # item.get_shape()


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_graphicsgridlayout(qtbot):
    layout = widgets.GraphicsGridLayout()
    item = widgets.GraphicsProxyWidget()
    button_1 = widgets.RadioButton("Test")
    qtbot.addWidget(button_1)
    item.setWidget(button_1)
    item2 = widgets.GraphicsProxyWidget()
    button_2 = widgets.RadioButton("Test")
    qtbot.addWidget(button_2)
    item2.setWidget(button_2)
    layout[1, 5:6] = item
    layout += item2
    layout.set_column_alignment(0, "left")
    with pytest.raises(InvalidParamError):
        layout.set_column_alignment(0, "test")
    layout.set_row_alignment(0, "left")
    with pytest.raises(InvalidParamError):
        layout.set_row_alignment(0, "test")
    assert len(layout) == 2
    layout.set_margin(0)


def test_graphicspixmapitem(qtbot):
    item = widgets.GraphicsPixmapItem()
    item.set_transformation_mode("smooth")
    assert item.get_transformation_mode() == "smooth"
    with pytest.raises(InvalidParamError):
        item.set_transformation_mode("test")
    item.set_shape_mode("bounding_rect")
    assert item.get_shape_mode() == "bounding_rect"
    with pytest.raises(InvalidParamError):
        item.set_shape_mode("test")
    assert item.get_pixmap() is None


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_graphicsscene(qtbot):
    scene = widgets.GraphicsScene()
    icon = iconprovider.get_icon("mdi.help-circle-outline")
    pixmap = icon.pixmap(200, 200)
    pixmap2 = icon.pixmap(20, 20)
    # item = widgets.GraphicsItem()
    g_1 = scene.add(pixmap)
    assert scene[0] == g_1
    g_2 = scene.add(pixmap2)
    assert scene.colliding_items(g_1, mode="intersects_bounding_rect") == [g_2]
    with pytest.raises(InvalidParamError):
        scene.colliding_items(g_1, mode="test")
    scene.add_line(core.LineF(0, 0, 1, 1))
    scene.add_line(core.Line(0, 0, 1, 1))
    scene.add_line((0, 0, 1, 1))
    scene.add_rect(core.Rect(0, 0, 1, 1))
    scene.add_rect(core.RectF(0, 0, 1, 1))
    scene.add_rect((0, 0, 1, 1), brush=gui.Brush(), pen=gui.Pen())
    scene.add_ellipse(core.Rect(0, 0, 1, 1))
    scene.add_ellipse(core.RectF(0, 0, 1, 1))
    scene.add_ellipse((0, 0, 1, 1), brush=gui.Brush(), pen=gui.Pen())
    poly = gui.PolygonF()
    poly.add_points((0, 0), (2, 0), (2, 1), (0, 1))
    scene.add_polygon(poly, brush=gui.Brush(), pen=gui.Pen())

    poly = gui.PolygonF()
    poly.add_points((0, 0), (2, 0), (2, 1), (0, 1))
    scene.add_polygon(poly)
    scene.add_pixmap(gui.Pixmap())
    path = gui.PainterPath()
    rect = core.RectF(0, 0, 1, 1)
    path.addRect(rect)
    scene.add_path(path, brush=gui.Brush(), pen=gui.Pen())
    scene.add_text("test", font=gui.Font())
    scene.add_simple_text("test")
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    scene.add_widget(widget)
    item = widgets.GraphicsRectItem(0, 0, 10, 10)
    scene.add_item_group(item)
    scene.set_item_index_method("none")
    assert scene.get_item_index_method() == "none"
    with pytest.raises(InvalidParamError):
        scene.set_item_index_method("test")


def test_graphicsrotation():
    rotation = widgets.GraphicsRotation()
    rotation.set_axis("z")
    with pytest.raises(InvalidParamError):
        rotation.set_axis("test")


def test_graphicsview(qtbot):
    view = widgets.GraphicsView()
    qtbot.addWidget(view)
    view.set_transformation_anchor("view_center")
    assert view.get_transformation_anchor() == "view_center"
    with pytest.raises(InvalidParamError):
        view.set_transformation_anchor("test")
    view.set_resize_anchor("view_center")
    assert view.get_resize_anchor() == "view_center"
    with pytest.raises(InvalidParamError):
        view.set_resize_anchor("test")
    view.set_viewport_update_mode("minimal")
    assert view.get_viewport_update_mode() == "minimal"
    with pytest.raises(InvalidParamError):
        view.set_viewport_update_mode("test")
    view.set_drag_mode("scroll_hand")
    assert view.get_drag_mode() == "scroll_hand"
    with pytest.raises(InvalidParamError):
        view.set_drag_mode("test")
    view.set_rubberband_selection_mode("intersects_shape")
    assert view.get_rubberband_selection_mode() == "intersects_shape"
    with pytest.raises(InvalidParamError):
        view.set_rubberband_selection_mode("test")
    view.set_cache_mode("background")
    assert view.get_cache_mode() == "background"
    with pytest.raises(InvalidParamError):
        view.set_cache_mode("test")


def test_gridlayout(qtbot):
    layout = widgets.GridLayout()
    layout2 = widgets.GridLayout()
    widget = widgets.RadioButton()
    layout[0:1, 0:3] = widget
    layout[5, 5] = layout2
    assert layout[0, 0] == widget
    assert layout[5, 5] == layout2
    layout.set_size_mode("maximum")
    layout.set_alignment("left")
    assert len(layout) == len(list(layout)) == 2
    layout += widgets.RadioButton()
    layout.set_origin_corner("bottom_right")
    assert layout.get_origin_corner() == "bottom_right"
    with pytest.raises(InvalidParamError):
        layout.set_origin_corner("test")


def test_groupbox(qtbot):
    widget = widgets.GroupBox()
    qtbot.addWidget(widget)
    widget.set_title("test_groupbox")
    ly = widgets.BoxLayout("horizontal")
    widget.set_layout(ly)
    ly += widgets.RadioButton("+=")
    widget.set_alignment("left")
    widget.set_enabled(False)


def test_headerview(qtbot):
    def test():
        pass

    table = widgets.TableView()
    qtbot.addWidget(table)
    model = widgets.FileSystemModel()
    table.set_model(model)
    header = widgets.HeaderView("horizontal", parent=table)
    qtbot.addWidget(header)
    table.setHorizontalHeader(header)
    header.set_resize_mode("interactive")
    header.set_resize_mode("interactive", col=0)
    with pytest.raises(InvalidParamError):
        header.set_resize_mode("test")
    header.resize_sections("interactive")
    header.set_context_menu_policy("custom")
    header.set_default_section_size(None)
    header.set_default_section_size(30)
    header.stretch_last_section()
    with pytest.raises(InvalidParamError):
        header.set_context_menu_policy("test")
    assert header.get_context_menu_policy() == "custom"
    header.set_custom_menu(test)
    header.set_sizes([100])
    assert len(header.get_section_labels()) == 4
    header.save_state()
    header.load_state()
    header.set_section_hidden(0, True)


def test_inputdialog(qtbot):
    dlg = widgets.InputDialog()
    qtbot.addWidget(dlg)
    dlg.set_input_mode("double")
    with pytest.raises(InvalidParamError):
        dlg.set_input_mode("test")
    assert dlg.get_input_mode() == "double"
    dlg.set_text_echo_mode("no_echo")
    with pytest.raises(InvalidParamError):
        dlg.set_text_echo_mode("test")
    assert dlg.get_text_echo_mode() == "no_echo"


def test_keysequenceedit(qtbot):
    seq = gui.KeySequence("Ctrl+A")
    edit = widgets.KeySequenceEdit(seq)
    edit.set_value("Ctrl+A")
    assert edit.get_value() == "Ctrl+A"
    assert edit.is_valid()


def test_label(qtbot):
    label = widgets.Label()
    qtbot.addWidget(label)
    label.set_image("")
    label.set_text("test_label")
    label.set_bold()
    label.set_italic()
    label.set_indent(4)
    label.set_weight("extra_light")
    label.set_point_size(14)
    label.set_color("red")
    label.set_color(None)
    with pytest.raises(InvalidParamError):
        label.set_weight("test")
    with pytest.raises(InvalidParamError):
        label.set_text_format("test")
    label.set_alignment(horizontal="left", vertical="top")
    label.set_alignment(vertical="bottom")
    label.set_alignment()
    label.set_text_interaction("by_mouse")
    expected = ["by_mouse", "like_text_editor", "like_text_browser"]
    assert label.get_text_interaction() == expected
    label.allow_links()
    with pytest.raises(InvalidParamError):
        label.set_text_interaction("test")
    # assert label.get_text_interaction() == "by_mouse"


def test_layoutitem(qtbot):
    item = widgets.LayoutItem()
    assert item.get_item() is None
    item.set_alignment("right")
    assert item.get_alignment() == "right"


def test_lcdnumber(qtbot):
    lcd = widgets.LCDNumber()
    qtbot.addWidget(lcd)
    lcd.set_value(500)
    assert lcd.get_value() == 500
    lcd.set_segment_style("filled")
    with pytest.raises(InvalidParamError):
        lcd.set_segment_style("test")
    assert lcd.get_segment_style() == "filled"
    lcd.set_mode("octal")
    with pytest.raises(InvalidParamError):
        lcd.set_mode("test")
    assert lcd.get_mode() == "octal"


def test_lineedit(qtbot):
    widget = widgets.LineEdit("test_lineedit")
    qtbot.addWidget(widget)
    widget.set_regex_validator("[0-9]")
    widget.set_font("Consolas")
    widget.set_text("0")
    widget.append_text("a")
    widget.set_echo_mode("password")
    with pytest.raises(InvalidParamError):
        widget.set_echo_mode("test")
    assert widget.get_echo_mode() == "password"
    widget.set_cursor_move_style("visual")
    with pytest.raises(InvalidParamError):
        widget.set_cursor_move_style("test")
    assert widget.get_cursor_move_style() == "visual"
    widget.set_input_mask("X")
    widget.set_range(0, 10)
    widget.set_value("5")
    widget += "append"


def test_listview(qtbot):
    widget = widgets.ListView()
    qtbot.addWidget(widget)
    widget.set_selection_mode(None)
    widget.set_selection_mode("single")
    widget.toggle_select_all()
    widget.set_selection_mode("multi")
    assert widget.get_selection_mode() == "multi"
    widget.set_view_mode("icon")
    with pytest.raises(InvalidParamError):
        widget.set_view_mode("test")
    assert widget.get_view_mode() == "icon"


def test_listwidget(qtbot):
    widget = widgets.ListWidget()
    qtbot.addWidget(widget)
    widget.add("test_listwidget", icon="mdi.timer")
    widget.add("test_listwidget", icon="mdi.timer")
    assert len(widget) == 2
    item = widget[0]
    assert item is not None
    widget.scroll_to_item(item, mode="ensure_visible")
    with pytest.raises(InvalidParamError):
        widget.scroll_to_item(item, mode="test")
    widget.on_index_change()
    widget.add_items(["a", "b"])
    widget.set_value("b")
    widget.sort()
    for item in widget:
        pass
    item = widgets.ListWidgetItem()
    widget += item
    del widget[0]
    widget.add_item(
        "Test",
        icon="mdi.timer",
        data={1: "Test"},
        foreground=gui.Brush(),
        background=gui.Brush(),
        font=gui.Font(),
        selected=True,
        status_tip="test",
        tool_tip="test",
        whats_this="test",
        checkstate="unchecked",
        size_hint=core.Size(10, 10),
        is_user_type=True,
    )


def test_listwidgetitem(qtbot):
    item = widgets.ListWidgetItem()
    item[constants.USER_ROLE] = "test"
    assert item[constants.USER_ROLE] == "test"
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(InvalidParamError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"
    item.get_background()
    item.get_foreground()
    item.get_font()
    item.get_icon()
    bytes(item)


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_mainwindow(qtbot):
    window = widgets.MainWindow()
    qtbot.addWidget(window)
    window.set_icon("mdi.timer")
    window.set_id("mainwindow")
    dockwidget = widgets.DockWidget()
    qtbot.addWidget(dockwidget)
    dockwidget.set_id("dockwidget")
    window.add_dockwidget(dockwidget, "left")
    widget = widgets.MainWindow()
    qtbot.addWidget(widget)
    widget.set_id("test")
    window.set_widget(widget)
    assert window["test"] == widget
    window.show()
    window.close()
    window.save_window_state(recursive=True)
    window.load_window_state(recursive=True)
    window.toggle_fullscreen()
    window.toggle_fullscreen()
    toolbar = widgets.ToolBar()
    qtbot.addWidget(toolbar)
    window.add_toolbar(toolbar)
    with pytest.raises(InvalidParamError):
        toolbar_2 = widgets.ToolBar()
        window.add_toolbar(toolbar_2, position="test")
    assert len(window.get_toolbars()) == 1
    assert len(window.get_docks()) == 1
    window.remove_dockwidgets([dockwidget])
    window.add_toolbar_break()
    with pytest.raises(InvalidParamError):
        window.add_toolbar_break("test")
    with window.edit_stylesheet() as ss:
        ss.QMainWindow.separator.setValues(width="1px", border="none")
    window.createPopupMenu()
    window.add_widget_as_dock("test", "Title")
    window.set_icon(None)


def test_mdiarea(qtbot):
    area = widgets.MdiArea()
    qtbot.addWidget(area)
    area.set_window_order("activation_history")
    with pytest.raises(InvalidParamError):
        area.set_window_order("test")
    assert area.get_window_order() == "activation_history"
    area.set_view_mode("default")
    with pytest.raises(InvalidParamError):
        area.set_view_mode("test")
    assert area.get_view_mode() == "default"
    area.set_tab_position("north")
    with pytest.raises(InvalidParamError):
        area.set_tab_position("test")
    assert area.get_tab_position() == "north"
    area.set_background("black")
    widget_1 = widgets.Widget()
    qtbot.addWidget(widget_1)
    area.add(widget_1)
    widget_2 = widgets.Widget()
    qtbot.addWidget(widget_2)
    area += widget_2
    sub = widgets.MdiSubWindow()
    qtbot.addWidget(sub)
    area.add(sub)


def test_menu(qtbot):
    menu = widgets.Menu("1", icon="mdi.timer")
    menu.add(widgets.Action(text="TestAction"))
    act = widgets.Action(text="TestAction")
    act.set_id("test")
    menu += act
    assert menu["test"] == act
    with pytest.raises(KeyError):
        menu["bla"]

    def test():
        pass

    menu.add_action(
        "test_menu",
        test,
        icon="mdi.timer",
        shortcut="Ctrl+A",
        checkable=True,
        status_tip="test",
    )
    assert len(menu) == 3
    for item in menu:
        pass
    menu.add_menu(widgets.Menu())
    menu.add_separator("test_menu")
    menu.add_separator()


def test_menubar(qtbot):
    menu = widgets.MenuBar()
    qtbot.addWidget(menu)
    menu += widgets.Action(text="TestAction")
    menu += widgets.Menu("TestMenu")
    menu.add_action(widgets.Action(text="TestAction 2"))
    menu.add_menu(widgets.Menu("TestMenu 2"))
    menu.add_separator()
    menu.add_action("test_menubar")
    menu.add_menu("test_menubar")


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_messagebox(qtbot):
    widget = widgets.MessageBox(buttons=["reset"])
    widget.set_icon("warning")
    widget.set_icon("mdi.timer")
    widget.add_button("ok")
    widget.set_text_format("rich")
    with pytest.raises(InvalidParamError):
        widget.set_text_format("test")
    assert widget.get_text_format() == "rich"
    with pytest.raises(InvalidParamError):
        widget.add_button("test")
    widget.get_standard_buttons()


def test_pangesture():
    gesture = widgets.PanGesture()
    gesture.get_delta()
    gesture.get_last_offset()
    gesture.get_offset()


def test_plaintextdocumentlayout():
    doc = gui.TextDocument()
    layout = widgets.PlainTextDocumentLayout(doc)
    repr(layout)
    assert len(layout) == 1
    layout.get_block_bounding_rect(gui.TextBlock())
    layout.get_frame_bounding_rect(gui.TextFrame(doc))


def test_plaintextedit(qtbot):
    widget = widgets.PlainTextEdit("This is a test")
    qtbot.addWidget(widget)
    with widget.create_cursor() as c:
        c.select_text(2, 4)
    with widget.current_cursor() as c:
        c.select_text(2, 4)
    widget.select_text(2, 4)
    widget.set_text("hallo")
    widget.set_disabled()
    widget.allow_wheel_zoom()
    widget.set_enabled()
    widget.set_font("Consolas")
    widget.append_text(" test")
    widget.append_text("test", newline=False)
    assert widget.text() == "hallo\n testtest"
    widget.highlight_current_line()
    widget.set_read_only()
    widget.scroll_to_top()
    widget.scroll_to_bottom()
    widget.set_value("test")
    widget.set_word_wrap_mode("anywhere")
    with pytest.raises(InvalidParamError):
        widget.set_word_wrap_mode("test")
    assert widget.get_word_wrap_mode() == "anywhere"
    widget.set_line_wrap_mode("widget_width")
    with pytest.raises(InvalidParamError):
        widget.set_line_wrap_mode("test")
    assert widget.get_line_wrap_mode() == "widget_width"
    assert widget.get_value() == "test"
    widget += "append"
    widget.set_regex_validator("[0-9]")


def test_pinchgesture():
    gesture = widgets.PinchGesture()
    gesture.get_start_center_point()
    gesture.get_center_point()
    gesture.get_last_center_point()
    gesture.set_change_flags(center_point=True)
    assert gesture.get_change_flags() == ["center_point"]
    gesture.set_total_change_flags(center_point=True)
    assert gesture.get_total_change_flags() == ["center_point"]


def test_progressbar(qtbot):
    bar = widgets.ProgressBar()
    qtbot.addWidget(bar)
    bar.set_alignment("left")
    bar.set_alignment("right")
    assert bar.get_alignment() == "right"
    with pytest.raises(InvalidParamError):
        bar.set_alignment("test")
    # assert bar.get_alignment() == "left"
    bar.set_text_direction("top_to_bottom")
    # assert bar.get_text_direction() == "top_to_bottom"
    with pytest.raises(InvalidParamError):
        bar.set_text_direction("test")
    bar.set_range(0, 20)
    # assert bar.get_text_direction() == "top_to_bottom"


# def test_progressdialog(qtbot):
#     widgets.ProgressDialog()


def test_pushbutton(qtbot):
    widget = widgets.PushButton("test_pushbutton", callback=print)
    qtbot.addWidget(widget)
    widget.set_text("test_pushbutton")
    widget.set_disabled()
    widget.set_enabled()
    assert widget.get_value() is False
    widget.set_icon("mdi.timer")
    widget.get_icon()
    widget.set_style_icon("titlebar_close_button")
    widget.set_icon_size(10)
    assert widget.get_icon_size() == core.Size(10, 10)
    widget.is_on = False
    assert widget.is_on is False
    widget.set_value(True)


def test_radiobutton(qtbot):
    widget = widgets.RadioButton("test_radiobutton")
    qtbot.addWidget(widget)
    widget.set_icon("mdi.timer")
    widget.set_enabled()
    widget.set_disabled()
    assert bool(widget) is False
    widget.set_value(True)
    assert widget.get_value() is True
    # widget.is_on = False
    # assert widget.is_on is False


def test_rubberband(qtbot):
    band = widgets.RubberBand("line")
    qtbot.addWidget(band)
    assert band.get_shape() == "line"


def test_scrollarea(qtbot):
    widget = widgets.ScrollArea()
    qtbot.addWidget(widget)
    widget.set_widget(widgets.Widget())


def test_scrollerproperties():
    properties = widgets.ScrollerProperties()
    properties["snap_time"] = 100
    with pytest.raises(InvalidParamError):
        properties.set_scroll_metric("test", 100)
    assert properties["snap_time"] == 100
    with pytest.raises(InvalidParamError):
        properties.get_scroll_metric("test")


def test_scroller(qtbot):
    w = widgets.PlainTextEdit()
    qtbot.addWidget(w)
    scroller = widgets.Scroller.get_scroller(w)
    assert scroller.get_state() == "inactive"
    scroller.get_velocity()
    scroller.get_pixel_per_meter()
    scroller.get_final_position()
    scroller.handle_input("move", core.PointF())
    with pytest.raises(InvalidParamError):
        scroller.handle_input("test", core.PointF())
    scroller.get_scroller_properties()
    assert widgets.Scroller.grab_gesture(w) == "tap"


def test_shortcut(qtbot):
    w = widgets.Widget()
    qtbot.addWidget(w)
    seq = gui.KeySequence("Ctrl+C")
    shortcut = widgets.Shortcut(seq, w)
    assert str(shortcut) == "Ctrl+C"
    shortcut.set_context("application")
    with pytest.raises(InvalidParamError):
        shortcut.set_context("test")
    assert shortcut.get_context() == "application"
    assert shortcut.get_key() == seq


def test_sizepolicy(qtbot):
    pol = widgets.SizePolicy()
    pol.set_control_type("toolbutton")
    assert pol.get_control_type() == "toolbutton"


def test_slider(qtbot):
    widget = widgets.Slider()
    qtbot.addWidget(widget)
    widget.set_horizontal()
    assert widget.is_horizontal()
    widget.set_vertical()
    assert widget.is_vertical()
    with pytest.raises(InvalidParamError):
        widget.set_tick_position("test")
    widget.set_tick_position("below")
    assert widget.get_tick_position() == "below"
    widget.set_orientation("horizontal")
    with pytest.raises(InvalidParamError):
        widget.set_orientation("test")
    assert widget.get_orientation() == "horizontal"


def test_statusbar(qtbot):
    widget = widgets.MainWindow()
    qtbot.addWidget(widget)
    status_bar = widgets.StatusBar()
    qtbot.addWidget(status_bar)
    label = widgets.Label("test_statusbar")
    qtbot.addWidget(label)
    status_bar.addWidget(label)
    status_bar.setup_default_bar()
    status_bar.show_message("test_statusbar")
    status_bar.add_action(widgets.Action())
    status_bar += widgets.Action()
    widget.setStatusBar(status_bar)
    status_bar.add_widget(widgets.Widget())
    status_bar += widgets.Widget()
    status_bar.add_widget(widgets.Widget(), permanent=True)


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_stackedlayout(qtbot):
    layout = widgets.StackedLayout()
    widget = widgets.RadioButton("test_stackedlayout")
    qtbot.addWidget(widget)
    layout += widget
    assert widget in layout
    layout.set_current_widget(widget)
    layout.set_size_mode("maximum")
    layout.set_margin(0)
    assert len(layout) == 1
    for item in layout:
        pass


def test_stackedwidget(qtbot):
    widget = widgets.StackedWidget()
    w = widgets.RadioButton("test_stackedwidget")
    widget += w
    assert widget[0] == w
    assert w in widget
    widget.set_current_widget(w)
    assert len(widget) == 1
    for item in widget:
        pass


def test_spaceritem(qtbot):
    item = widgets.SpacerItem(0, 0, "expanding", "expanding")
    item.change_size(0, 0)


def test_spinbox(qtbot):
    widget = widgets.SpinBox(default_value=5)
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    widget.set_value(10)
    widget.set_special_value("test_spinbox")
    with pytest.raises(InvalidParamError):
        widget.set_button_symbols("test")
    with pytest.raises(InvalidParamError):
        widget.set_correction_mode("test")
    with pytest.raises(InvalidParamError):
        widget.set_step_type("test")
    assert widget.is_valid()
    assert widget.get_value() == 10


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_splashscreen(qtbot):
    pixmap = gui.Pixmap.create_dot()
    scr = widgets.SplashScreen(path=pixmap, width=100)
    qtbot.addWidget(scr)
    with scr:
        pass
    scr.set_text("test")


def test_splitter(qtbot):
    widget = widgets.Splitter("vertical")
    qtbot.addWidget(widget)
    test = widgets.Label("test_splitter")
    qtbot.addWidget(widget)
    test2 = widgets.Label("test_splitter")
    qtbot.addWidget(widget)
    widget.add_widget(test)
    widget += test2
    assert len(widget) == 2
    assert widget[0] == test
    for item in widget:
        pass
    widget.set_size_policy("expanding", "expanding")
    widget.set_orientation("horizontal")
    with pytest.raises(InvalidParamError):
        widget.set_orientation("test")
    widget.add_layout(widgets.BoxLayout("horizontal"))
    widgets.Splitter.from_widgets(widgets.Widget())
    test3 = widgets.Label("test_splitter")
    widget[0] = test3


def test_styleoptionslider(qtbot):
    slider = widgets.StyleOptionSlider()
    slider.is_vertical()
    slider.set_horizontal()
    slider.set_vertical()


def test_swipegesture():
    gesture = widgets.SwipeGesture()
    assert gesture.get_horizontal_direction() == "right"
    assert gesture.get_vertical_direction() == "none"


def test_systemtrayicon(qtbot):
    icon = widgets.SystemTrayIcon()
    icon.set_icon("mdi.folder")
    icon.show_message("test", "", "critical")
    icon.show_message("test", "", "mdi.folder")
    icon.show_message("test", "")


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_tabwidget(qtbot):
    widget = widgets.TabWidget(detachable=True)
    qtbot.addWidget(widget)
    widget1 = widgets.Widget()
    widget.add_tab(widget1, "mdi.timer", show=True)
    widget.set_document_mode(True)
    widget2 = widgets.Widget()
    widget.add_tab(widget2, "test_tabwidget", "mdi.timer", position=0, show=True)
    assert len(widget) == 2
    w = widgets.Widget()
    widget.add_tab(w, "test_tabwidget", "mdi.timer")
    assert widget[2] == w
    widget.set_tab(0, "right", None)
    widget.set_detachable()
    widget.detach_tab(0, core.Point())
    with pytest.raises(InvalidParamError):
        widget.set_tab_shape("test")
    widget.remove_tab(1)
    layout = widgets.BoxLayout("horizontal")
    widget.add_tab(layout, "mdi.timer")
    widget.set_icon_size(10)
    widget.set_icon_size((10, 10))
    widget.set_icon_size(core.Size(10, 10))
    widget.close_detached_tabs()
    # widget.close_detached_tabs()


def test_tapgesture():
    gesture = widgets.TapGesture()
    gesture.get_position()


def test_tapandholdgesture():
    gesture = widgets.TapAndHoldGesture()
    gesture.get_position()


def test_textbrowser(qtbot):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(b"Test")
    tmp.close()
    path = pathlib.Path(tempfile.gettempdir()) / tmp.name
    widget = widgets.TextBrowser()
    widget.set_markdown("test")
    widget.set_markdown_file(str(path))
    # widget.set_rst("test")
    # widget.set_rst_file(str(path))
    os.unlink(str(path))


def test_textedit(qtbot):
    widget = widgets.TextEdit()
    qtbot.addWidget(widget)
    widget.set_text("test")
    widget.append_text(" this")
    assert widget.text() == "test\n this"
    with widget.create_cursor() as c:
        c.select_text(1, 3)
    widget.select_text(1, 3)
    widget.set_font("Consolas")
    widget.set_enabled()
    widget.set_read_only()
    widget.scroll_to_bottom()
    widget.set_disabled()
    widget.set_background_color("black")
    widget.set_text_color("red")
    widget += "append"


def test_timeedit(qtbot):
    widget = widgets.TimeEdit()
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    widget.set_range(datetime.time(1, 1, 1), datetime.time(3, 3, 3))
    widget.set_value(datetime.time(0, 0, 0))
    assert widget.get_time() == widget.min_time()
    assert widget.max_time() == datetime.time(3, 3, 3)
    dt = datetime.time(2, 2, 2)
    widget.set_value(dt)
    assert widget.get_value() == dt


def test_toolbar(qtbot):
    widget = widgets.ToolBar()
    qtbot.addWidget(widget)
    widget.add_menu_button("test,", "mdi.timer", menu=widgets.Menu())
    widget.set_style("icon")
    widget.add_separator("Test")
    widget.add_separator()
    widget.add_spacer()
    assert widget.get_style() == "icon"
    widget.set_font_size(10)
    widget.set_enabled()
    widget.set_disabled()
    widget.set_icon_size(10)
    assert widget.get_icon_size() == core.Size(10, 10)
    assert widget.is_area_allowed("top")
    with pytest.raises(InvalidParamError):
        widget.is_area_allowed("test")
    assert widget.get_allowed_areas() == ["left", "right", "top", "bottom", "all"]

    def test():
        pass

    widget.add_action("test", "mdi.timer", test, checkable=True)


def test_toolbutton(qtbot):
    widget = widgets.ToolButton()
    qtbot.addWidget(widget)
    widget.set_disabled()
    widget.set_enabled()
    widget.set_shortcut("Ctrl+A")
    widget.set_icon_size(20)
    action = widgets.Action()
    widget.set_default_action(action)
    with pytest.raises(InvalidParamError):
        widget.set_popup_mode("test")
    assert widget.get_popup_mode() == "delayed"
    with pytest.raises(InvalidParamError):
        widget.set_arrow_type("test")
    widget.set_arrow_type("left")
    with pytest.raises(InvalidParamError):
        widget.set_style("test")
    widget.set_style("text_below_icon")
    assert widget.get_arrow_type() == "left"
    menu = widgets.Menu()
    act = widgets.Action()
    act.set_id("test")
    menu.add(act)
    widget.setMenu(menu)
    assert widget["test"] == act


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_tooltip(qtbot):
    widgets.ToolTip.show_text(text="test")


def test_tabbar(qtbot):
    widget = widgets.TabBar()
    qtbot.addWidget(widget)
    widget.set_icon_size(10)
    assert widget.get_icon_size() == core.Size(10, 10)
    with pytest.raises(InvalidParamError):
        widget.set_selection_behavior_on_remove("test")
    assert widget.get_remove_behaviour() == "left_tab"
    with pytest.raises(InvalidParamError):
        widget.set_elide_mode("test")


def test_tableview(qtbot):
    widget = widgets.TableView()
    qtbot.addWidget(widget)
    widget.set_selection_mode("extended")
    with pytest.raises(InvalidParamError):
        widget.set_selection_mode("test")
    widget.set_selection_behaviour("rows")
    assert widget.get_selection_behaviour() == "rows"
    with pytest.raises(InvalidParamError):
        widget.set_selection_behaviour("test")
    widget.set_horizontal_scrollbar_policy("always_on")
    widget.set_vertical_scrollbar_policy("always_on")
    widget.set_horizontal_scrollbar_width(12)
    widget.set_vertical_scrollbar_width(12)
    widget.set_edit_triggers(None)
    widget.set_edit_triggers("edit_key")
    widget.sort_by_column(0)
    with pytest.raises(InvalidParamError):
        widget.set_edit_triggers("test")
    widget.selectAll()
    widget.current_index()
    widget.current_data()
    widget.adapt_sizes()
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.num_selected()
    widget.jump_to_column(0)
    # widget.select_last_row()
    widget.set_scroll_mode("item")
    widget.set_vertical_scroll_mode("item")
    widget.set_horizontal_scroll_mode("item")
    with pytest.raises(InvalidParamError):
        widget.set_scroll_mode("aa")
    with pytest.raises(InvalidParamError):
        widget.set_vertical_scroll_mode("aa")
    with pytest.raises(InvalidParamError):
        widget.set_horizontal_scroll_mode("aa")
    widget.highlight_when_inactive()
    widget.set_table_color("black")
    widget.scroll_to_bottom()
    widget.selected_data()
    widget.selected_rows()
    widget.selected_names()
    assert len(widget.selected_indexes()) == 0
    widget.get_edit_triggers()
    assert widget.h_header is not None
    header = widgets.HeaderView("vertical", parent=widget)
    qtbot.addWidget(header)
    widget.v_header = header
    assert widget.v_header is not None


@pytest.mark.skipif(sys.platform == "linux", reason="Only supported on windows")
def test_tablewidget(qtbot, tablewidget):
    # qtbot.addWidget(tablewidget)
    tablewidget.sort()
    item = widgets.TableWidgetItem("test")
    tablewidget[0, 0] = item
    assert tablewidget[0, 0] == item
    del tablewidget[0, 0]


def test_tablewidgetitem(qtbot):
    item = widgets.TableWidgetItem()
    item[constants.USER_ROLE] = "test"
    assert item[constants.USER_ROLE] == "test"
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(InvalidParamError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"
    item.get_background()
    item.get_foreground()
    item.get_font()
    item.get_icon()


def test_tablewidgetselectionrange():
    range_1 = widgets.TableWidgetSelectionRange(5, 5, 15, 15)
    range_2 = widgets.TableWidgetSelectionRange(0, 0, 20, 20)
    result = widgets.TableWidgetSelectionRange(0, 0, 20, 20)
    assert result == range_1 | range_2
    result = widgets.TableWidgetSelectionRange(5, 5, 15, 15)
    assert result == range_1 & range_2
    assert repr(result) == "TableWidgetSelectionRange(5, 5, 15, 15)"


def test_toolbox(qtbot):
    w = widgets.RadioButton("test1")
    w2 = widgets.RadioButton("test2")
    qtbot.addWidget(w)
    qtbot.addWidget(w2)
    w2.set_id("test_name")
    widget = widgets.ToolBox()
    qtbot.addWidget(widget)
    widget.add_widget(w, "title", "mdi.timer")
    widget.add_widget(w2)
    assert widget["test_name"] == w2
    for w in widget:
        pass
    assert widget[1] == w2
    del widget[1]


def test_treeview(qtbot):
    widget = widgets.TreeView()
    qtbot.addWidget(widget)
    assert len(widget) == 0
    model = widgets.FileSystemModel()
    widget.set_model(model)
    widget.selectAll()
    widget.h_header
    # widget.h_scrollbar
    widget.v_scrollbar
    widget.set_size_adjust_policy("content")
    with pytest.raises(InvalidParamError):
        widget.set_size_adjust_policy("test")
    assert widget.get_size_adjust_policy() == "content"
    widget.set_scrollbar_policy("always_on")
    with pytest.raises(InvalidParamError):
        widget.set_scrollbar_policy("test")
    widget.set_scrollbar_width(10)
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.sort_by_column(0)
    widget.scroll_to_top()
    widget.current_index()
    widget.set_selection_mode("extended")
    widget.set_drag_drop_mode("drop")
    widget.set_selection_behaviour("rows")
    widget.set_horizontal_scrollbar_policy("always_on")
    widget.set_vertical_scrollbar_policy("always_on")
    with pytest.raises(InvalidParamError):
        widget.set_horizontal_scrollbar_policy("test")
    with pytest.raises(InvalidParamError):
        widget.set_vertical_scrollbar_policy("test")
    widget.set_horizontal_scrollbar_width(12)
    widget.set_vertical_scrollbar_width(12)
    widget.num_selected()
    widget.jump_to_column(0)
    widget.highlight_when_inactive()
    widget.raise_dock()
    widget.adapt_sizes()
    model = gui.StandardItemModel()
    model.add("test")
    widget.set_model(model)
    widget.set_delegate(widgets.StyledItemDelegate())
    widget.set_delegate(widgets.StyledItemDelegate(), column=0, persistent=True)
    widget.set_delegate(widgets.StyledItemDelegate(), row=0, persistent=True)
    widget.toggle_select_all()
    widget.toggle_select_all()
    model.update_row(0)


def test_treewidget(qtbot):
    widget = widgets.TreeWidget()
    qtbot.addWidget(widget)
    widget.sort()


def test_treewidgetitem(qtbot):
    item = widgets.TreeWidgetItem()
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(InvalidParamError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"
    item.get_background()
    item.get_foreground()
    item.get_font()
    item.get_icon()
    item.set_child_indicator_policy("dont_show")
    with pytest.raises(InvalidParamError):
        item.set_child_indicator_policy("test")
    assert item.get_child_indicator_policy() == "dont_show"
    bytes(item)
    child = widgets.TreeWidgetItem()
    item += child
    for child in item:
        pass
    assert len(item) == 1
    assert item[0] == child
    item.sort_children(0)
    del item[0]


def test_treewidgetitemiterator(qtbot):
    item = widgets.TreeWidget()
    widgets.TreeWidgetItemIterator(
        item,
        flags=None,
        hidden=True,
        selected=True,
        selectable=True,
        draggable=True,
        droppable=True,
        has_children=True,
        checked=True,
        enabled=True,
        editable=True,
        user_flag=True,
    )


def test_undoview(qtbot):
    view = widgets.UndoView()
    qtbot.addWidget(view)
    stack = gui.UndoStack()
    cmd = stack.add_command("test", redo=lambda: print("a"), undo=lambda: print("b"))
    view.set_clean_icon("mdi.folder")
    view.set_value(stack)
    assert view[0] == cmd


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_whatsthis(qtbot):
    with widgets.WhatsThis.enter_mode():
        pass


@pytest.mark.skipif(sys.platform == "linux", reason="X11 connection break")
def test_widget(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    widget.set_tooltip("test")
    widget.set_cursor("caret")
    widget.set_min_width(100)
    widget.set_min_width(None)
    widget.set_max_width(100)
    widget.set_max_width(None)
    widget.set_min_height(200)
    widget.set_min_height(None)
    widget.set_max_height(200)
    widget.set_max_height(None)
    widget.set_font_size(20)
    widget.get_font_metrics()
    widget.get_font_info()
    widget.set_id("test")
    widget.set_unique_id()
    widget.get_palette()
    widget.set_attribute("native_window")
    widget.set_attributes(native_window=False)
    with pytest.raises(InvalidParamError):
        widget.set_attribute("test")
    with pytest.raises(InvalidParamError):
        widget.set_cursor("test")
    widget.set_focus_policy("strong")
    assert widget.get_focus_policy() == "strong"
    with pytest.raises(InvalidParamError):
        widget.set_focus_policy("test")
    layout = widgets.BoxLayout()
    widget.set_layout(layout)
    with pytest.raises(ValueError):
        widget.set_layout("test")
    with widget.block_signals():
        pass
    with widget.edit_font():
        pass
    with widget.edit_stylesheet():
        pass
    with widget.edit_palette():
        pass
    widget.get_font()
    widget.set_enabled()
    widget.set_disabled()
    widget.set_min_size(1, 1)
    widget.set_max_size(2, 2)
    widget.set_title("test")
    assert widget.get_title() == "test"
    with widget.updates_off():
        widget.set_title("test2")
    widget.enabled = True
    assert widget.enabled is True
    widget.set_modality("window")
    with pytest.raises(InvalidParamError):
        widget.set_modality("test")
    assert widget.get_modality() == "window"
    widget.center()
    widget_2 = widgets.Widget()
    qtbot.addWidget(widget_2)
    widget_2.set_layout("horizontal", margin=2)
    widget_3 = widgets.Widget()
    qtbot.addWidget(widget_3)
    widget_3.set_layout("form")
    widget_4 = widgets.Widget()
    qtbot.addWidget(widget_4)
    widget_4.set_layout("stacked")
    widget_5 = widgets.Widget()
    qtbot.addWidget(widget_5)
    widget_5.set_layout("flow")
    widget_5.set_margin(2)
    widget_5.set_window_state("fullscreen")
    widget_5.set_mask((0, 0, 10, 10), "ellipse")
    with pytest.raises(InvalidParamError):
        widget_5.set_window_state("test")
    assert widget_5.get_window_state() == "fullscreen"


def test_widgetaction(qtbot):
    action = widgets.Action()
    widgetaction = widgets.WidgetAction(parent=action)
    widgetaction.set_tooltip("test")
    widgetaction.set_enabled()
    widgetaction.set_disabled()
    widgetaction.set_icon("mdi.timer")
    widgetaction.set_shortcut("Ctrl+A")


def test_wizard(qtbot):
    w = widgets.Wizard()
    qtbot.addWidget(w)
    w.add_widget_as_page(widgets.Widget())
    pix = gui.Pixmap(100, 100)
    w.set_pixmap("background", pix)
    with pytest.raises(InvalidParamError):
        w.set_pixmap("test", pix)
    assert bytes(w.get_pixmap("background")) == bytes(pix)
    with pytest.raises(InvalidParamError):
        w.get_pixmap("test")
    w.set_wizard_style("mac")
    with pytest.raises(InvalidParamError):
        w.set_wizard_style("test")
    assert w.get_wizard_style() == "mac"
    w.set_button_text("back", "test")
    with pytest.raises(InvalidParamError):
        w.set_button_text("test", "test")
    assert w.get_button_text("back") == "test"
    with pytest.raises(InvalidParamError):
        w.get_button_text("test")
    w.get_button("back")
    with pytest.raises(InvalidParamError):
        w.get_button("test")
    w.set_title_format("auto")
    with pytest.raises(InvalidParamError):
        w.set_title_format("test")
    assert w.get_title_format() == "auto"
    w.set_subtitle_format("auto")
    with pytest.raises(InvalidParamError):
        w.set_subtitle_format("test")
    assert w.get_subtitle_format() == "auto"
    w.set_option("help_button_on_right", True)
    with pytest.raises(InvalidParamError):
        w.set_option("test", True)
    assert w.get_option("help_button_on_right") is True
    with pytest.raises(InvalidParamError):
        w.get_option("test")


def test_wizardpage(qtbot):
    page = widgets.WizardPage()
    qtbot.addWidget(page)
    pix = gui.Pixmap(100, 100)
    page.set_pixmap("background", pix)
    with pytest.raises(InvalidParamError):
        page.set_pixmap("test", pix)
    assert bytes(page.get_pixmap("background")) == bytes(pix)
    with pytest.raises(InvalidParamError):
        page.get_pixmap("test")
    page.set_button_text("back", "test")
    with pytest.raises(InvalidParamError):
        page.set_button_text("test", "test")
    assert page.get_button_text("back") == "test"
    with pytest.raises(InvalidParamError):
        page.get_button_text("test")
