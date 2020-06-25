#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import datetime
import pickle

import pytest
from qtpy import QtCore

from prettyqt import core, gui, widgets


def test_action():
    action = widgets.Action()
    action.set_tooltip("test")
    action.set_enabled()
    action.set_disabled()
    action.set_icon(None)
    action.set_icon("mdi.timer")
    action.set_shortcut("Ctrl+A")
    with open("data.pkl", "wb") as jar:
        pickle.dump(action, jar)
    with open("data.pkl", "rb") as jar:
        action = pickle.load(jar)
    assert action.shortcut().toString() == "Ctrl+A"
    assert action.toolTip() == "test"
    action.set_priority("low")
    assert action.get_priority() == "low"
    action.set_shortcut_context("widget_with_children")
    assert action.get_shortcut_context() == "widget_with_children"
    action.set_menu(widgets.Menu())


def test_boxlayout():
    layout = widgets.BoxLayout("horizontal", margin=0)
    widget = widgets.RadioButton("test")
    layout += widget
    layout2 = widgets.BoxLayout("horizontal")
    layout += layout2
    assert layout[1] == layout2
    layout.set_size_mode("maximum")
    assert layout.get_size_mode() == "maximum"
    layout.set_alignment("left")
    # assert layout.get_alignment() == "left"
    with pytest.raises(ValueError):
        layout.set_size_mode("bla")
    layout.set_margin(0)
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)
    assert len(layout) == 2
    repr(layout)
    layout.add_stretch(1)
    layout.add_spacing(1)


def test_buttongroup():
    widget = widgets.ButtonGroup()
    btn = widgets.RadioButton("test")
    widget.addButton(btn, id=2)
    assert widget[2] == btn


def test_calendarwiget():
    widget = widgets.CalendarWidget()
    assert widget.get_date() == widget.get_value()
    widget.set_selection_mode("single")
    assert widget.get_selection_mode() == "single"
    with pytest.raises(ValueError):
        widget.set_selection_mode("test")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_checkbox():
    widget = widgets.CheckBox()
    widget.set_disabled()
    widget.set_enabled()
    import pickle
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    assert bool(widget) is False
    widget.set_value(True)
    assert widget.get_value() is True
    repr(widget)
    with pytest.raises(ValueError):
        widget.set_checkstate("test")
    widget.is_on = False
    assert widget.is_on is False


def test_colordialog():
    dlg = widgets.ColorDialog()
    assert str(dlg.current_color()) == str(gui.Color("white"))
    with open("data.pkl", "wb") as jar:
        pickle.dump(dlg, jar)
    with open("data.pkl", "rb") as jar:
        dlg = pickle.load(jar)


def test_combobox():
    box = widgets.ComboBox()
    box.set_disabled()
    box.set_enabled()
    box.add("test", data="data", icon="mdi.timer")
    assert len(box) == 1
    box.set_insert_policy("bottom")
    assert box.get_insert_policy() == "bottom"
    with pytest.raises(ValueError):
        box.set_insert_policy("bla")
    box.set_size_adjust_policy("first_show")
    with pytest.raises(ValueError):
        box.set_size_adjust_policy("bla")
    assert box.get_size_adjust_policy() == "first_show"
    box.set_icon_size(10)
    box.set_min_char_length(10)
    with open("data.pkl", "wb") as jar:
        pickle.dump(box, jar)
    with open("data.pkl", "rb") as jar:
        box = pickle.load(jar)
    box.add("test2", data="data", icon="mdi.timer")
    box.set_text("test2")
    assert box.text() == "test2"


def test_commandlinkbutton():
    widget = widgets.CommandLinkButton("Test")
    widget.set_disabled()
    widget.set_enabled()
    widget.set_icon("mdi.timer")
    with pytest.raises(ValueError):
        widget.set_style_icon("bla")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)


def test_dateedit():
    widget = widgets.DateEdit()
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.date(2000, 11, 11)
    widget.set_value(dt)
    assert widget.get_value() == dt
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)


def test_datetimeedit():
    widget = widgets.DateTimeEdit()
    widget.set_disabled()
    widget.set_enabled()
    dt = datetime.datetime(2000, 11, 11)
    widget.set_value(dt)
    widget.set_format("dd.MM.yyyy")
    assert widget.get_value() == dt
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)


def test_desktopwidget():
    widgets.DesktopWidget()


def test_dialog(qtbot):
    dlg = widgets.Dialog(layout="horizontal")
    qtbot.addWidget(dlg)
    qtbot.keyPress(dlg, QtCore.Qt.Key_F11)
    dlg.delete_on_close()
    dlg.add_widget(widgets.RadioButton("test"))
    dlg.set_icon("mdi.timer")
    with open("data.pkl", "wb") as jar:
        pickle.dump(dlg, jar)
    with open("data.pkl", "rb") as jar:
        dlg = pickle.load(jar)
    dlg.resize(0, 400)
    dlg.resize((0, 400))
    dlg.add_buttonbox()


def test_dialogbuttonbox():
    box = widgets.DialogButtonBox()
    box.set_horizontal()
    box.set_vertical()
    btn = box.add_default_button("apply")
    with pytest.raises(ValueError):
        btn = box.add_default_button("test")
    box.set_orientation("horizontal")
    with pytest.raises(ValueError):
        box.set_orientation("test")
    assert box.get_orientation() == "horizontal"
    box.add_button("test", callback=print)
    assert len(box) == 2
    assert btn == box["apply"]
    assert "apply" in box
    for item in box:
        pass
    btn = box.add_default_buttons(["ok"])


def test_dockwidget():
    widget = widgets.DockWidget()
    widget.setup_title_bar()
    widget.maximise()
    w = widgets.Widget()
    widget.set_widget(w)
    w.raise_dock()


def test_doublespinbox():
    widget = widgets.DoubleSpinBox(default_value=5)
    widget.set_disabled()
    widget.set_enabled()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)


def test_filedialog():
    dlg = widgets.FileDialog()
    dlg.set_label_text("accept", "test")
    dlg.set_accept_mode("open")
    with pytest.raises(ValueError):
        dlg.set_accept_mode("bla")
    dlg.set_accept_mode("save")
    dlg.set_extension_filter(dict(a=[".csv"]))
    dlg.set_filter("all_dirs")
    with pytest.raises(ValueError):
        dlg.set_filter("test")
    dlg.selected_file()
    dlg.selected_files()
    with open("data.pkl", "wb") as jar:
        pickle.dump(dlg, jar)
    with open("data.pkl", "rb") as jar:
        dlg = pickle.load(jar)


def test_filesystemmodel(qtmodeltester):
    model = widgets.FileSystemModel()
    idx = model.index(0, 0)
    data = model.data(idx, model.DATA_ROLE)
    print(data)
    model.yield_child_indexes(idx)
    # modeltest.ModelTest(model)
    # qtmodeltester.check(model, force_py=False)


def test_fontdialog():
    widgets.FontDialog()


def test_formlayout():
    widget = widgets.FormLayout()
    widget.set_size_mode("maximum")
    with pytest.raises(ValueError):
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
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    assert len(widget) == 2
    repr(widget)


def test_frame():
    widgets.Frame()


def test_gridlayout():
    layout = widgets.GridLayout()
    widget = widgets.RadioButton()
    layout[0:1, 0:3] = widget
    assert layout[0, 0] == widget
    layout.set_size_mode("maximum")
    layout.set_alignment("left")
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)
    assert len(layout) == len(list(layout)) == 1
    repr(layout)
    layout += widgets.RadioButton()


def test_groupbox():
    widget = widgets.GroupBox()
    widget.set_title("test")
    ly = widgets.BoxLayout("horizontal")
    widget.set_layout(ly)
    ly += widgets.RadioButton("+=")
    widget.set_alignment("left")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.set_enabled(False)
    repr(widget)


def test_headerview():

    def test():
        pass

    table = widgets.TableView()
    model = widgets.FileSystemModel()
    table.setModel(model)
    header = widgets.HeaderView(parent=table)
    table.setHorizontalHeader(header)
    header.resize_mode("interactive")
    header.resize_mode("interactive", col=0)
    with pytest.raises(ValueError):
        header.resize_mode("test")
    header.resize_sections("interactive")
    header.set_contextmenu_policy("custom")
    header.set_default_section_size(None)
    header.set_default_section_size(30)
    header.stretch_last_section()
    with pytest.raises(ValueError):
        header.set_contextmenu_policy("test")
    assert header.get_contextmenu_policy() == "custom"
    header.set_custom_menu(test)
    header.set_sizes([100])
    assert header.section_labels() == ['Name', 'Size', 'Type', 'Date Modified']
    header.save_state()
    header.load_state()
    header.set_section_hidden(0, True)


def test_keysequenceedit():
    seq = gui.KeySequence("Ctrl+A")
    edit = widgets.KeySequenceEdit(seq)
    edit.set_value("Ctrl+A")
    assert edit.get_value() == "Ctrl+A"
    assert edit.is_valid()
    repr(edit)


def test_label():
    label = widgets.Label()
    label.set_image("")
    label.set_text("testus")
    with pytest.raises(ValueError):
        label.set_text_format("test")
    label.set_alignment(horizontal="left", vertical="top")
    label.set_alignment(vertical="bottom")
    label.set_text_interaction("by_mouse")
    expected = ['by_mouse', 'like_text_editor', 'like_text_browser']
    assert label.get_text_interaction() == expected
    label.allow_links()
    with pytest.raises(ValueError):
        label.set_text_interaction("test")
    # assert label.get_text_interaction() == "by_mouse"
    with open("data.pkl", "wb") as jar:
        pickle.dump(label, jar)
    with open("data.pkl", "rb") as jar:
        label = pickle.load(jar)
    repr(label)


def test_lineedit():
    widget = widgets.LineEdit("Test")
    widget.set_regex_validator("[0-9]")
    widget.set_font("Consolas")
    widget.set_text("0")
    widget.append_text("a")
    widget.set_echo_mode("password")
    with pytest.raises(ValueError):
        widget.set_echo_mode("test")
    assert widget.get_echo_mode() == "password"
    widget.set_input_mask("X")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)
    widget.set_range(0, 10)
    widget.set_value("5")
    widget += "append"


def test_listview():
    widget = widgets.ListView()
    widget.set_selection_mode(None)
    widget.set_selection_mode("single")
    widget.toggle_select_all()
    widget.set_selection_mode("multi")
    assert widget.get_selection_mode() == "multi"
    widget.set_view_mode("icon")
    with pytest.raises(ValueError):
        widget.set_view_mode("test")
    assert widget.get_view_mode() == "icon"


def test_listwidget():
    widget = widgets.ListWidget()
    widget.add("test", icon="mdi.timer")
    widget.add("test", icon="mdi.timer")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    assert len(widget) == 2
    item = widget[0]
    assert item is not None
    widget.scroll_to_item(item, mode="ensure_visible")
    with pytest.raises(ValueError):
        widget.scroll_to_item(item, mode="test")
    widget.on_index_change()
    widget.add_items(["a", "b"])
    widget.set_value("b")
    for item in widget:
        pass
    item = widgets.ListWidgetItem()
    widget += item
    repr(widget)


def test_listwidgetitem():
    item = widgets.ListWidgetItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(item, jar)
    with open("data.pkl", "rb") as jar:
        item = pickle.load(jar)
    repr(item)
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(ValueError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"


def test_mainwindow():
    window = widgets.MainWindow()
    window.set_icon("mdi.timer")
    w = widgets.DockWidget()
    window.add_dockwidget(w, "left")
    window.show()
    window.close()
    window.load_window_state()
    window.toggle_fullscreen()
    window.toggle_fullscreen()
    window.add_toolbar(widgets.ToolBar())
    with pytest.raises(ValueError):
        window.add_toolbar(widgets.ToolBar(), position="test")
    assert len(window.get_toolbars()) == 1
    assert len(window.get_docks()) == 1
    window.remove_dockwidgets([w])
    window.add_toolbar_break()
    ss = dict(width="1px", border="none")
    window.set_stylesheet("QMainWindow::separator", ss)
    window.createPopupMenu()
    window.add_widget_as_dock("test", "Title")
    with open("data.pkl", "wb") as jar:
        pickle.dump(window, jar)
    with open("data.pkl", "rb") as jar:
        window = pickle.load(jar)
    window.set_icon(None)


def test_mdiarea():
    area = widgets.MdiArea()
    area.set_window_order("activation")
    with pytest.raises(ValueError):
        area.set_window_order("test")
    assert area.get_window_order() == "activation"
    area.set_view_mode("default")
    with pytest.raises(ValueError):
        area.set_view_mode("test")
    assert area.get_view_mode() == "default"
    area.set_tab_position("north")
    with pytest.raises(ValueError):
        area.set_tab_position("test")
    assert area.get_tab_position() == "north"
    area.set_background("black")
    area.add(widgets.Widget())


def test_menu():
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

    menu.add_action("test", test,
                    icon="mdi.timer",
                    shortcut="Ctrl+A",
                    checkable=True,
                    status_tip="test")
    assert len(menu) == 3
    for item in menu:
        pass
    menu.add_menu(widgets.Menu())
    menu.add_separator("test")
    menu.add_separator()


def test_menubar():
    menu = widgets.MenuBar()
    menu += widgets.Action(text="TestAction")
    menu += widgets.Menu("TestMenu")
    menu.add_action(widgets.Action(text="TestAction 2"))
    menu.add_menu(widgets.Menu("TestMenu 2"))
    menu.add_separator()
    menu.add_action("test")
    menu.add_menu("test")


def test_messagebox():
    widget = widgets.MessageBox(buttons=["reset"])
    widget.set_icon("warning")
    widget.set_icon("mdi.timer")
    widget.add_button("ok")
    widget.set_text_format("rich")
    with pytest.raises(ValueError):
        widget.set_text_format("test")
    with pytest.raises(ValueError):
        widget.add_button("test")
    assert widget.get_text_format() == "rich"
    widget.get_standard_buttons()


def test_plaintextedit():
    widget = widgets.PlainTextEdit("This is a test")
    with widget.create_cursor() as c:
        c.select_text(2, 4)
    widget.select_text(2, 4)
    widget.set_text("hallo")
    widget.set_disabled()
    widget.set_enabled()
    widget.set_font("Consolas")
    widget.append_text(" test")
    assert widget.text() == "hallo\n test"
    widget.highlight_current_line()
    widget.set_read_only()
    widget.get_result_widget()
    widget.scroll_to_top()
    widget.scroll_to_bottom()
    widget.set_value("test")
    widget.set_wrap_mode("anywhere")
    with pytest.raises(ValueError):
        widget.set_wrap_mode("test")
    assert widget.get_value() == "test"
    widget += "append"
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_progressbar():
    bar = widgets.ProgressBar()
    bar.set_alignment("left")
    bar.set_alignment("right")
    with pytest.raises(ValueError):
        bar.set_alignment("test")
    # assert bar.get_alignment() == "left"
    bar.set_text_direction("top_to_bottom")
    with pytest.raises(ValueError):
        bar.set_text_direction("test")
    bar.set_range(0, 20)
    # assert bar.get_text_direction() == "top_to_bottom"


def test_progressdialog():
    widgets.ProgressDialog()


def test_pushbutton():
    widget = widgets.PushButton("Test", callback=print)
    widget.set_text("test")
    widget.set_disabled()
    widget.set_enabled()
    assert widget.get_value() is False
    widget.set_icon("mdi.timer")
    widget.set_style_icon("close")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.is_on = False
    assert widget.is_on is False
    widget.set_value(True)


def test_radiobutton():
    widget = widgets.RadioButton("Test")
    widget.set_icon("mdi.timer")
    widget.set_enabled()
    widget.set_disabled()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    assert bool(widget) is False
    repr(widget)
    widget.set_value(True)
    assert widget.get_value() is True
    # widget.is_on = False
    # assert widget.is_on is False


def test_scrollarea():
    widget = widgets.ScrollArea()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.set_widget(widgets.Widget())


def test_slider():
    widget = widgets.Slider()
    widget.set_horizontal()
    assert widget.is_horizontal()
    widget.set_vertical()
    assert widget.is_vertical()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    with pytest.raises(ValueError):
        widget.set_tick_position("test")
    widget.set_tick_position("right")


def test_statusbar():
    widget = widgets.MainWindow()
    status_bar = widgets.StatusBar()
    status_bar.set_color("black")
    label = widgets.Label("test")
    status_bar.addWidget(label)
    status_bar.setup_default_bar()
    status_bar.show_message("test")
    status_bar.add_action(widgets.Action())
    status_bar += widgets.Action()
    widget.setStatusBar(status_bar)
    status_bar.add_widget(widgets.Widget())
    status_bar += widgets.Widget()
    status_bar.add_widget(widgets.Widget(), permanent=True)


def test_stackedlayout():
    layout = widgets.StackedLayout()
    widget = widgets.RadioButton("test")
    layout += widget
    layout.set_size_mode("maximum")
    layout.set_margin(0)
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)
    assert len(layout) == 1
    for item in layout:
        pass
    return True


def test_spinbox():
    widget = widgets.SpinBox(default_value=5)
    widget.set_disabled()
    widget.set_enabled()
    widget.set_value(10)
    widget.set_special_value("test")
    assert widget.is_valid()
    assert widget.get_value() == 10
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    repr(widget)


def test_splashscreen():
    scr = widgets.SplashScreen(path="", width=100)
    with scr:
        pass
    scr.set_text("test")


def test_splitter():
    widget = widgets.Splitter("vertical")
    test = widgets.Label("test")
    test2 = widgets.Label("test2")
    widget.add_widget(test)
    widget += test2
    assert len(widget) == 2
    assert widget[0] == test
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    for item in widget:
        pass
    widget.set_size_policy("expanding", "expanding")
    widget.set_orientation("horizontal")
    with pytest.raises(ValueError):
        widget.set_orientation("test")
    widget.add_layout(widgets.BoxLayout("horizontal"))
    widgets.Splitter.from_widgets([widgets.Widget()])


def test_styleoptionslider():
    slider = widgets.StyleOptionSlider()
    slider.is_vertical()
    slider.set_horizontal()
    slider.set_vertical()


def test_tabwidget():
    widget = widgets.TabWidget(detachable=True)
    widget.add_tab(widgets.Widget(), "mdi.timer", show=True)
    widget.set_document_mode(True)
    widget.insert_tab(0, widgets.Widget(), "test", "mdi.timer", show=True)
    assert len(widget) == 2
    w = widgets.Widget()
    widget.add_tab(w, "test", "mdi.timer")
    assert widget[2] == w
    widget.set_tab(0, "right", None)
    widget.set_detachable()
    widget.detach_tab(0, core.Point())
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    with pytest.raises(ValueError):
        widget.set_tab_shape("test")
    widget.remove_tab(0)
    widget.add_tab(widgets.BoxLayout("horizontal"), "mdi.timer")
    widget.close_detached_tabs()
    # widget.close_detached_tabs()


def test_textbrowser():
    widget = widgets.TextBrowser()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.set_markdown("test")
    widget.set_rst("test")


def test_textedit():
    widget = widgets.TextEdit()
    widget.set_text("test")
    with widget.create_cursor() as c:
        c.select_text(1, 3)
    widget.select_text(1, 3)
    widget.append_text(" this")
    assert widget.text() == "test\n this"
    widget.set_font("Consolas")
    widget.set_enabled()
    widget.set_read_only()
    widget.scroll_to_bottom()
    widget.set_disabled()
    widget.set_color("black")
    widget.set_text_color("red")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget += "append"


def test_timeedit():
    widget = widgets.TimeEdit()
    widget.set_disabled()
    widget.set_enabled()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.set_range(datetime.time(1, 1, 1), datetime.time(3, 3, 3))
    widget.set_value(datetime.time(0, 0, 0))
    assert widget.get_time() == widget.min_time()
    assert widget.max_time() == datetime.time(3, 3, 3)
    dt = datetime.time(2, 2, 2)
    widget.set_value(dt)
    assert widget.get_value() == dt


def test_toolbar():
    widget = widgets.ToolBar()
    widget.add_menu_button("test,", "mdi.timer", menu=widgets.Menu())
    widget.set_style("icon")
    widget.set_style(None)
    assert widget.get_style() == "icon"
    widget.set_font_size(10)
    widget.set_enabled()
    widget.set_disabled()
    assert widget.is_area_allowed("top")
    with pytest.raises(ValueError):
        widget.is_area_allowed("test")

    def test():
        pass

    widget.add_action("test", "mdi.timer", test, checkable=True)


def test_toolbutton():
    widget = widgets.ToolButton()
    widget.set_disabled()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.set_enabled()
    widget.set_shortcut("Ctrl+A")
    with pytest.raises(ValueError):
        widget.set_popup_mode("test")
    assert widget.get_popup_mode() == "delayed"
    with pytest.raises(ValueError):
        widget.set_arrow_type("test")
    widget.set_arrow_type("left")
    assert widget.get_arrow_type() == "left"
    menu = widgets.Menu()
    act = widgets.Action()
    act.id = "test"
    menu.add(act)
    widget.setMenu(menu)
    assert widget["test"] == act


def test_tabbar():
    widget = widgets.TabBar()
    widget.set_icon_size(20)
    with pytest.raises(ValueError):
        widget.set_remove_behaviour("test")
    assert widget.get_remove_behaviour() == "left_tab"
    with pytest.raises(ValueError):
        widget.set_elide_mode("test")


def test_tableview():
    widget = widgets.TableView()
    widget.set_selection_mode("extended")
    with pytest.raises(ValueError):
        widget.set_selection_mode("test")
    widget.set_selection_behaviour("rows")
    assert widget.get_selection_behaviour() == "rows"
    with pytest.raises(ValueError):
        widget.set_selection_behaviour("test")
    widget.set_horizontal_scrollbar_policy("always_on")
    widget.set_vertical_scrollbar_policy("always_on")
    widget.set_horizontal_scrollbar_width(12)
    widget.set_vertical_scrollbar_width(12)
    widget.set_edit_triggers(None)
    widget.set_edit_triggers("edit_key")
    with pytest.raises(ValueError):
        widget.set_edit_triggers("test")
    widget.selectAll()
    widget.current_index()
    widget.current_data()
    widget.adapt_sizes()
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.num_selected()
    widget.jump_to_column(0)
    widget.set_scroll_mode("item")
    widget.set_vertical_scroll_mode("item")
    widget.set_horizontal_scroll_mode("item")
    with pytest.raises(ValueError):
        widget.set_scroll_mode("aa")
    with pytest.raises(ValueError):
        widget.set_vertical_scroll_mode("aa")
    with pytest.raises(ValueError):
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


def test_tablewidget():
    widget = widgets.TableWidget()
    widget.sort()


def test_toolbox():
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
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_treeview():
    widget = widgets.TreeView()
    assert len(widget) == 0
    model = widgets.FileSystemModel()
    widget.setModel(model)
    widget.selectAll()
    widget.h_header
    # widget.h_scrollbar
    widget.v_scrollbar
    widget.set_size_adjust_policy("content")
    with pytest.raises(ValueError):
        widget.set_size_adjust_policy("test")
    assert widget.get_size_adjust_policy() == "content"
    widget.set_scrollbar_policy("always_on")
    with pytest.raises(ValueError):
        widget.set_scrollbar_policy("test")
    widget.set_scrollbar_width(10)
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.scroll_to_top()
    widget.current_index()
    widget.set_selection_mode("extended")
    widget.set_selection_behaviour("rows")
    widget.set_horizontal_scrollbar_policy("always_on")
    widget.set_vertical_scrollbar_policy("always_on")
    with pytest.raises(ValueError):
        widget.set_horizontal_scrollbar_policy("test")
    with pytest.raises(ValueError):
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
    widget.setModel(model)
    widget.set_delegate(widgets.StyledItemDelegate())
    widget.set_delegate(widgets.StyledItemDelegate(), column=0, persistent=True)
    widget.set_delegate(widgets.StyledItemDelegate(), row=0, persistent=True)
    widget.toggle_select_all()
    widget.toggle_select_all()
    model.update_row(0)


def test_treewidget():
    widget = widgets.TreeWidget()
    widget.sort()


def test_treewidgetitem():
    item = widgets.TreeWidgetItem()
    repr(item)
    with open("data.pkl", "wb") as jar:
        pickle.dump(item, jar)
    with open("data.pkl", "rb") as jar:
        item = pickle.load(jar)
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(ValueError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"


def test_widget():
    widget = widgets.Widget()
    widget.set_tooltip("test")
    layout = widgets.BoxLayout()
    widget.set_layout(layout)
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
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
    with pytest.raises(ValueError):
        widget.set_modality("test")
    assert widget.get_modality() == "window"
    widget.center()
    widget.set_layout("horizontal")
    widget.set_layout("form")
    widget.set_layout("stacked")
    widget.set_layout("flow")


def test_widgetaction():
    action = widgets.Action()
    widgetaction = widgets.WidgetAction(parent=action)
    widgetaction.set_tooltip("test")
    widgetaction.set_enabled()
    widgetaction.set_disabled()
    widgetaction.set_icon("mdi.timer")
    widgetaction.set_shortcut("Ctrl+A")
    return True


def test_wizard():
    w = widgets.Wizard()
    w.add_widget_as_page(widgets.Widget())


def test_wizardpage():
    widgets.WizardPage()
