#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import inspect
import datetime
import pickle

# import logging
import tempfile
import pathlib
import os

import pytest
from qtpy import QtCore

from prettyqt import core, gui, widgets, constants
from prettyqt.utils import InvalidParamError

clsmembers = inspect.getmembers(widgets, inspect.isclass)
clsmembers = [tpl for tpl in clsmembers if not tpl[0].startswith("Abstract")]
clsmembers = [tpl for tpl in clsmembers if core.Object in tpl[1].mro()]

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
    if core.VersionNumber.get_qt_version() >= (5, 14, 0):
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


def test_buttongroup(qtbot):
    widget = widgets.ButtonGroup()
    btn = widgets.RadioButton("test")
    widget.addButton(btn, id=2)
    assert widget[2] == btn


def test_calendarwiget(qtbot):
    widget = widgets.CalendarWidget()
    assert widget.get_date() == widget.get_value()
    widget.set_value(datetime.date(2000, 10, 10))
    widget.set_selection_mode(None)
    widget.set_selection_mode("single")
    assert widget.get_selection_mode() == "single"
    with pytest.raises(InvalidParamError):
        widget.set_selection_mode("test")


def test_checkbox(qtbot):
    widget = widgets.CheckBox()
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
    assert str(dlg.current_color()) == str(gui.Color("white"))


def test_combobox(qtbot):
    box = widgets.ComboBox()
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
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.date(2000, 11, 11)
    widget.set_value(dt)
    assert widget.get_value() == dt


def test_datetimeedit(qtbot):
    widget = widgets.DateTimeEdit()
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.datetime(2000, 11, 11)
    widget.set_value(dt)
    widget.set_format("dd.MM.yyyy")
    assert widget.get_value() == dt


def test_desktopwidget(qtbot):
    widgets.DesktopWidget()


def test_dialog(qtbot, qttester):
    dlg = widgets.Dialog(layout="horizontal")
    qtbot.addWidget(dlg)
    dlg.show()
    qttester.send_keypress(dlg, QtCore.Qt.Key_F11)
    dlg.delete_on_close()
    dlg.add_widget(widgets.RadioButton("test"))
    dlg.set_icon("mdi.timer")
    dlg.resize(200, 400)
    dlg.resize((150, 400))
    dlg.add_buttonbox()


def test_dialogbuttonbox(qtbot):
    box = widgets.DialogButtonBox()
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


def test_dockwidget(qtbot):
    widget = widgets.DockWidget()
    widget.setup_title_bar()
    widget.maximise()
    w = widgets.Widget()
    widget.set_widget(w)
    w.raise_dock()


def test_doublespinbox(qtbot):
    widget = widgets.DoubleSpinBox(default_value=5)
    widget.set_disabled()
    widget.set_enabled()


def test_filedialog(qtbot):
    dlg = widgets.FileDialog(path_id="test", extension_filter=dict(test=["*.test"]))
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


def test_filesystemmodel(qtmodeltester):
    model = widgets.FileSystemModel()
    model.set_root_path("/")
    idx = model.index(0, 0)
    model.get_paths([idx])
    model.data(idx, model.DATA_ROLE)
    model.yield_child_indexes(idx)
    if core.VersionNumber.get_qt_version() >= (5, 14, 0):
        model.watch_for_changes(False)
        model.use_custom_icons(False)
    model.resolve_sym_links(False)
    model.set_name_filters(["test"], hide=True)
    model.set_filter("drives")
    with pytest.raises(InvalidParamError):
        model.set_filter("test")
    # modeltest.ModelTest(model)
    # qtmodeltester.check(model, force_py=False)


def test_fontcombobox(qtbot):
    widget = widgets.FontComboBox()
    font = widget.get_current_font()
    assert font == widget.get_value()
    widget.set_font_filters("scalable")
    assert widget.get_font_filters() == ["scalable"]
    with pytest.raises(InvalidParamError):
        widget.set_font_filters("test")


def test_fontdialog(qtbot):
    dlg = widgets.FontDialog()
    dlg.get_current_font()


def test_formlayout(qtbot):
    widget = widgets.FormLayout()
    widget.set_size_mode("maximum")
    with pytest.raises(InvalidParamError):
        widget.set_size_mode("bla")
    widget[0, "left"] = "0, left"
    widget[1, "left"] = widgets.RadioButton("1, left")
    widget[0, "right"] = "label 1 right"
    widget[1, "right"] = widgets.RadioButton("1, right")
    widget[2] = "by str"
    widget[3] = widgets.RadioButton("widget[3]")
    widget += widgets.RadioButton("added with +=")
    widget += ("added with +=", widgets.RadioButton("tuple"))
    widget = widgets.FormLayout.build_from_dict({"from": "dict"})
    assert len(widget) == 2


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
    item.set_focus("active_window")
    with pytest.raises(InvalidParamError):
        item.set_focus("test")
    item[0] = "test"
    assert item[0] == "test"
    # item.get_shape()


def test_graphicsgridlayout():
    layout = widgets.GraphicsGridLayout()
    item = widgets.GraphicsProxyWidget()
    item.setWidget(widgets.RadioButton("Test"))
    item2 = widgets.GraphicsProxyWidget()
    item2.setWidget(widgets.RadioButton("Test"))
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


def test_graphicsscene(qtbot):
    scene = widgets.GraphicsScene()
    icon = gui.icon.get_icon("mdi.help-circle-outline")
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
    poly = gui.Polygon()
    poly.add_points((0, 0), (2, 0), (2, 1), (0, 1))
    scene.add_polygon(poly, brush=gui.Brush(), pen=gui.Pen())
    # poly = gui.Polygon()
    # poly.add_points((0, 0), (2, 0), (2, 1), (0, 1))
    # scene.add_polygon(poly)
    scene.add_pixmap(gui.Pixmap())
    path = gui.PainterPath()
    rect = core.RectF(0, 0, 1, 1)
    path.addRect(rect)
    scene.add_path(path, brush=gui.Brush(), pen=gui.Pen())
    scene.add_text("test", font=gui.Font())
    scene.add_simple_text("test")
    scene.add_widget(widgets.Widget())
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


def test_groupbox(qtbot):
    widget = widgets.GroupBox()
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
    model = widgets.FileSystemModel()
    table.set_model(model)
    header = widgets.HeaderView("horizontal", parent=table)
    table.setHorizontalHeader(header)
    header.set_resize_mode("interactive")
    header.set_resize_mode("interactive", col=0)
    with pytest.raises(InvalidParamError):
        header.set_resize_mode("test")
    header.resize_sections("interactive")
    header.set_contextmenu_policy("custom")
    header.set_default_section_size(None)
    header.set_default_section_size(30)
    header.stretch_last_section()
    with pytest.raises(InvalidParamError):
        header.set_contextmenu_policy("test")
    assert header.get_contextmenu_policy() == "custom"
    header.set_custom_menu(test)
    header.set_sizes([100])
    assert header.get_section_labels() == ["Name", "Size", "Type", "Date Modified"]
    header.save_state()
    header.load_state()
    header.set_section_hidden(0, True)


def test_keysequenceedit(qtbot):
    seq = gui.KeySequence("Ctrl+A")
    edit = widgets.KeySequenceEdit(seq)
    edit.set_value("Ctrl+A")
    assert edit.get_value() == "Ctrl+A"
    assert edit.is_valid()


def test_label(qtbot):
    label = widgets.Label()
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


def test_lcdnumber(qtbot):
    lcd = widgets.LCDNumber()
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
    widget.set_regex_validator("[0-9]")
    widget.set_font("Consolas")
    widget.set_text("0")
    widget.append_text("a")
    widget.set_echo_mode("password")
    with pytest.raises(InvalidParamError):
        widget.set_echo_mode("test")
    assert widget.get_echo_mode() == "password"
    widget.set_input_mask("X")
    widget.set_range(0, 10)
    widget.set_value("5")
    widget += "append"


def test_listview(qtbot):
    widget = widgets.ListView()
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


def test_mainwindow(qtbot):
    window = widgets.MainWindow()
    window.set_icon("mdi.timer")
    window.set_id("mainwindow")
    dockwidget = widgets.DockWidget()
    dockwidget.set_id("dockwidget")
    window.add_dockwidget(dockwidget, "left")
    widget = widgets.MainWindow()
    widget.set_id("test")
    window.set_widget(widget)
    assert window["test"] == widget
    window.show()
    window.close()
    window.save_window_state(recursive=True)
    window.load_window_state(recursive=True)
    window.toggle_fullscreen()
    window.toggle_fullscreen()
    window.add_toolbar(widgets.ToolBar())
    with pytest.raises(InvalidParamError):
        window.add_toolbar(widgets.ToolBar(), position="test")
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
    area.add(widgets.Widget())
    area += widgets.Widget()
    sub = widgets.MdiSubWindow()
    area.add(sub)


def test_menu(qtbot):
    menu = widgets.Menu("1", icon="mdi.timer")
    menu.add(widgets.Action(text="TestAction"))
    act = widgets.Action(text="TestAction")
    act.id = "test"
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
    menu += widgets.Action(text="TestAction")
    menu += widgets.Menu("TestMenu")
    menu.add_action(widgets.Action(text="TestAction 2"))
    menu.add_menu(widgets.Menu("TestMenu 2"))
    menu.add_separator()
    menu.add_action("test_menubar")
    menu.add_menu("test_menubar")


def test_messagebox(qtbot):
    widget = widgets.MessageBox(buttons=["reset"])
    widget.set_icon("warning")
    widget.set_icon("mdi.timer")
    widget.add_button("ok")
    widget.set_text_format("rich")
    with pytest.raises(InvalidParamError):
        widget.set_text_format("test")
    with pytest.raises(InvalidParamError):
        widget.add_button("test")
    assert widget.get_text_format() == "rich"
    widget.get_standard_buttons()


def test_plaintextdocumentlayout():
    doc = gui.TextDocument()
    layout = widgets.PlainTextDocumentLayout(doc)
    repr(layout)
    assert len(layout) == 1
    layout.get_block_bounding_rect(gui.TextBlock())
    layout.get_frame_bounding_rect(gui.TextFrame(doc))


def test_plaintextedit(qtbot):
    widget = widgets.PlainTextEdit("This is a test")
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
    widget.set_wrap_mode("anywhere")
    with pytest.raises(InvalidParamError):
        widget.set_wrap_mode("test")
    widget.set_line_wrap_mode("widget_width")
    with pytest.raises(InvalidParamError):
        widget.set_line_wrap_mode("test")
    assert widget.get_value() == "test"
    widget += "append"
    widget.set_regex_validator("[0-9]")


def test_progressbar(qtbot):
    bar = widgets.ProgressBar()
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


def test_progressdialog(qtbot):
    widgets.ProgressDialog()


def test_pushbutton(qtbot):
    widget = widgets.PushButton("test_pushbutton", callback=print)
    widget.set_text("test_pushbutton")
    widget.set_disabled()
    widget.set_enabled()
    assert widget.get_value() is False
    widget.set_icon("mdi.timer")
    widget.set_style_icon("titlebar_close_button")
    widget.is_on = False
    assert widget.is_on is False
    widget.set_value(True)


def test_radiobutton(qtbot):
    widget = widgets.RadioButton("test_radiobutton")
    widget.set_icon("mdi.timer")
    widget.set_enabled()
    widget.set_disabled()
    assert bool(widget) is False
    widget.set_value(True)
    assert widget.get_value() is True
    # widget.is_on = False
    # assert widget.is_on is False


def test_scrollarea(qtbot):
    widget = widgets.ScrollArea()
    widget.set_widget(widgets.Widget())


def test_scrollerproperties():
    properties = widgets.ScrollerProperties()
    properties["snap_time"] = 100
    with pytest.raises(InvalidParamError):
        properties.set_scroll_metric("test", 100)
    assert properties["snap_time"] == 100
    with pytest.raises(InvalidParamError):
        properties.get_scroll_metric("test")


def test_scroller():
    w = widgets.PlainTextEdit()
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


def test_sizepolicy(qtbot):
    pol = widgets.SizePolicy()
    pol.set_control_type("toolbutton")
    assert pol.get_control_type() == "toolbutton"


def test_slider(qtbot):
    widget = widgets.Slider()
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
    status_bar = widgets.StatusBar()
    label = widgets.Label("test_statusbar")
    status_bar.addWidget(label)
    status_bar.setup_default_bar()
    status_bar.show_message("test_statusbar")
    status_bar.add_action(widgets.Action())
    status_bar += widgets.Action()
    widget.setStatusBar(status_bar)
    status_bar.add_widget(widgets.Widget())
    status_bar += widgets.Widget()
    status_bar.add_widget(widgets.Widget(), permanent=True)


def test_stackedlayout(qtbot):
    layout = widgets.StackedLayout()
    widget = widgets.RadioButton("test_stackedlayout")
    layout += widget
    assert widget in layout
    layout.set_current_widget(widget)
    layout.set_size_mode("maximum")
    layout.set_margin(0)
    assert len(layout) == 1
    for item in layout:
        pass


def test_spaceritem(qtbot):
    item = widgets.SpacerItem(0, 0, "expanding", "expanding")
    item.change_size(0, 0)


def test_spinbox(qtbot):
    widget = widgets.SpinBox(default_value=5)
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


def test_splashscreen(qtbot):
    pixmap = gui.Pixmap.create_dot()
    scr = widgets.SplashScreen(path=pixmap, width=100)
    with scr:
        pass
    scr.set_text("test")


def test_splitter(qtbot):
    widget = widgets.Splitter("vertical")
    test = widgets.Label("test_splitter")
    test2 = widgets.Label("test_splitter")
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


def test_systemtrayicon(qtbot):
    icon = widgets.SystemTrayIcon()
    icon.set_icon("mdi.folder")
    icon.show_message("test", "", "critical")
    icon.show_message("test", "", "mdi.folder")
    icon.show_message("test", "")


def test_tabwidget(qtbot):
    widget = widgets.TabWidget(detachable=True)
    widget.add_tab(widgets.Widget(), "mdi.timer", show=True)
    widget.set_document_mode(True)
    widget.add_tab(widgets.Widget(), "test_tabwidget", "mdi.timer", position=0, show=True)
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
    widget.add_tab(widgets.BoxLayout("horizontal"), "mdi.timer")
    widget.close_detached_tabs()
    # widget.close_detached_tabs()


def test_textbrowser(qtbot):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(b"Test")
    tmp.close()
    path = pathlib.Path(tempfile.gettempdir()) / tmp.name
    widget = widgets.TextBrowser()
    if core.VersionNumber.get_qt_version() >= (5, 14, 0):
        widget.set_markdown("test")
        widget.set_markdown_file(str(path))
    widget.set_rst("test")
    widget.set_rst_file(str(path))
    os.unlink(str(path))


def test_textedit(qtbot):
    widget = widgets.TextEdit()
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
    widget.add_menu_button("test,", "mdi.timer", menu=widgets.Menu())
    widget.set_style("icon")
    widget.set_style(None)
    widget.add_separator("Test")
    widget.add_separator()
    widget.add_spacer()
    assert widget.get_style() == "icon"
    widget.set_font_size(10)
    widget.set_enabled()
    widget.set_disabled()
    assert widget.is_area_allowed("top")
    with pytest.raises(InvalidParamError):
        widget.is_area_allowed("test")

    def test():
        pass

    widget.add_action("test", "mdi.timer", test, checkable=True)


def test_toolbutton(qtbot):
    widget = widgets.ToolButton()
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
    act.id = "test"
    menu.add(act)
    widget.setMenu(menu)
    assert widget["test"] == act


def test_tooltip(qtbot):
    widgets.ToolTip.show_text(text="test")


def test_tabbar(qtbot):
    widget = widgets.TabBar()
    widget.set_icon_size(20)
    with pytest.raises(InvalidParamError):
        widget.set_selection_behavior_on_remove("test")
    assert widget.get_remove_behaviour() == "left_tab"
    with pytest.raises(InvalidParamError):
        widget.set_elide_mode("test")


def test_tableview(qtbot):
    widget = widgets.TableView()
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
    widget.v_header = widgets.HeaderView("vertical", parent=widget)
    assert widget.v_header is not None


def test_tablewidget(qtbot, tablewidget):
    tablewidget.sort()
    item = widgets.TableWidgetItem("test")
    tablewidget[0, 0] = item
    assert tablewidget[0, 0] == item


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


def test_toolbox(qtbot):
    w = widgets.RadioButton("test1")
    w2 = widgets.RadioButton("test2")
    w2.id = "test_name"
    widget = widgets.ToolBox()
    widget.add_widget(w, "title", "mdi.timer")
    widget.add_widget(w2)
    assert widget["test_name"] == w2
    for w in widget:
        pass
    assert widget[1] == w2


def test_treeview(qtbot):
    widget = widgets.TreeView()
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


def test_undocommand():
    cmd = widgets.UndoCommand()
    cmd2 = widgets.UndoCommand(cmd)
    assert cmd[0] == cmd2
    assert len(cmd) == 1


def test_undostack():
    stack = widgets.UndoStack()
    cmd = stack.add_command("test", redo=lambda: print("a"), undo=lambda: print("b"))
    assert stack[0] == cmd
    assert len(stack) == 1
    with stack.create_macro("test"):
        pass


def test_undogroup():
    group = widgets.UndoGroup()
    stack = widgets.UndoStack()
    group.addStack(stack)
    assert len(group) == 1
    assert group[0] == stack


def test_undoview(qtbot):
    view = widgets.UndoView()
    stack = widgets.UndoStack()
    cmd = stack.add_command("test", redo=lambda: print("a"), undo=lambda: print("b"))
    view.set_clean_icon("mdi.folder")
    view.set_value(stack)
    assert view[0] == cmd


def test_widget(qtbot):
    widget = widgets.Widget()
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
    widget.set_enabled()
    widget.set_disabled()
    widget.set_min_size(1, 1)
    widget.set_max_size(2, 2)
    widget.title = "test"
    assert widget.title == "test"
    with widget.updates_off():
        widget.set_title("test2")
    widget.enabled = True
    assert widget.enabled is True
    widget.set_modality("window")
    with pytest.raises(InvalidParamError):
        widget.set_modality("test")
    assert widget.get_modality() == "window"
    widget.center()
    widget = widgets.Widget()
    widget.set_layout("horizontal", margin=2)
    widget = widgets.Widget()
    widget.set_layout("form")
    widget = widgets.Widget()
    widget.set_layout("stacked")
    widget = widgets.Widget()
    widget.set_layout("flow")
    widget.set_margin(2)


def test_widgetaction(qtbot):
    action = widgets.Action()
    widgetaction = widgets.WidgetAction(parent=action)
    widgetaction.set_tooltip("test")
    widgetaction.set_enabled()
    widgetaction.set_disabled()
    widgetaction.set_icon("mdi.timer")
    widgetaction.set_shortcut("Ctrl+A")
    return True


def test_wizard(qtbot):
    w = widgets.Wizard()
    w.add_widget_as_page(widgets.Widget())


def test_wizardpage(qtbot):
    widgets.WizardPage()
