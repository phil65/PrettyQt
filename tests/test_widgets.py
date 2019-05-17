#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import datetime

from qtpy import QtCore

from prettyqt import core, gui, widgets


def test_action():
    action = widgets.Action()
    action.set_tooltip("test")
    action.set_enabled()
    action.set_disabled()
    action.set_icon("mdi.timer")
    action.set_shortcut("Ctrl+A")
    with open("data.pkl", "wb") as jar:
        pickle.dump(action, jar)
    with open("data.pkl", "rb") as jar:
        action = pickle.load(jar)
    assert action.shortcut().toString() == "Ctrl+A"
    assert action.toolTip() == "test"


def test_boxlayout():
    layout = widgets.BoxLayout("horizontal")
    widget = widgets.RadioButton("test")
    layout += widget
    layout.set_size_mode("maximum")
    layout.set_margin(0)
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)
    assert len(layout) == 1
    repr(layout)


def test_buttongroup():
    widget = widgets.ButtonGroup()
    btn = widgets.RadioButton("test")
    widget.addButton(btn, id=2)
    assert widget[2] == btn


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
    box.add_item("test", data="data", icon="mdi.timer")
    box.set_insert_policy("bottom")
    box.set_size_policy("first_show")
    box.set_icon_size(10)
    box.set_min_char_length(10)
    with open("data.pkl", "wb") as jar:
        pickle.dump(box, jar)
    with open("data.pkl", "rb") as jar:
        box = pickle.load(jar)
    repr(box)


def test_commandlinkbutton():
    widget = widgets.CommandLinkButton("Test")
    widget.set_disabled()
    widget.set_enabled()
    widget.set_icon("mdi.timer")
    widget.set_style_icon("close")
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
    dlg.set_modality()
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
    btn = box.add_button("apply")
    assert len(box) == 1
    assert btn == box["apply"]
    for item in box:
        pass


def test_dockwidget():
    widget = widgets.DockWidget()
    widget.setup_title_bar()
    widget.maximise()


def test_doublespinbox():
    widget = widgets.DoubleSpinBox()
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
    dlg.set_accept_mode("save")
    dlg.set_filter(dict(a=[".csv"]))
    dlg.selected_file()
    dlg.selected_files()
    with open("data.pkl", "wb") as jar:
        pickle.dump(dlg, jar)
    with open("data.pkl", "rb") as jar:
        dlg = pickle.load(jar)


def test_filesystemmodel():
    model = widgets.FileSystemModel()
    idx = model.index(0, 0)
    data = model.data(idx, model.DATA_ROLE)
    print(data)
    model.yield_child_indexes(idx)
    # qtmodeltester.check(model, force_py=True)


def test_fontdialog():
    widgets.FontDialog()


def test_formlayout():
    widget = widgets.FormLayout()
    widget.set_size_mode("maximum")
    widget[0, "left"] = "0, left"
    widget[1, "left"] = widgets.RadioButton("1, left")
    widget[0, "right"] = "label 1 right"
    widget[1, "right"] = widgets.RadioButton("1, right")
    widget[2] = "by str"
    widget[3] = widgets.RadioButton("widget[3]")
    widget += widgets.RadioButton("added with +=")
    widget += ("added with +=", widgets.RadioButton("tuple"))
    widget = widgets.FormLayout.from_dict({"from": "dict"})
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


def test_groupbox():
    widget = widgets.GroupBox()
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
    header.resize_sections("interactive")
    header.set_contextmenu_policy("custom")
    header.set_custom_menu(test)
    header.set_sizes([100])
    label = header.section_labels()
    print(label)


def test_label():
    label = widgets.Label()
    label.set_image("")
    label.set_alignment(horizontal="left", vertical="top")
    label.set_text_interaction("by_mouse")
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
    widget.set_input_mask("X")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_listview():
    widget = widgets.ListView()
    widget.set_selection_mode("single")
    widget.toggle_select_all()
    widget.set_selection_mode("multi")
    assert widget.get_selection_mode() == "multi"


def test_listwidget():
    widget = widgets.ListWidget()
    widget.add_item("test", icon="mdi.timer")
    widget.add_item("test", icon="mdi.timer")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    assert len(widget) == 2
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
    ss = dict(width="1px", border="none")
    window.set_stylesheet("QMainWindow::separator", ss)
    window.add_widget_as_dock("test", "Title")
    with open("data.pkl", "wb") as jar:
        pickle.dump(window, jar)
    with open("data.pkl", "rb") as jar:
        window = pickle.load(jar)


def test_menu():
    menu = widgets.Menu("1")

    def test():
        pass

    menu.add_action("test", test, icon="mdi.timer", shortcut="Ctrl+A", checkable=True)
    menu._separator("test")


def test_menubar():
    menu = widgets.MenuBar()
    menu += widgets.Action("test")


def test_messagebox():
    widget = widgets.MessageBox()
    widget.set_icon("mdi.timer")


def test_plaintextedit():
    widget = widgets.PlainTextEdit()
    widget.set_text("hallo")
    widget.set_disabled()
    widget.set_enabled()
    widget.set_font("Consolas")
    widget.append_text(" test")
    assert widget.text() == "hallo\n test"
    widget.highlight_current_line()
    widget.set_read_only()
    widget.get_result_widget()
    widget.scroll_to_bottom()
    widget.set_value("test")
    assert widget.get_value() == "test"
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_progressbar():
    widgets.ProgressBar()


def test_progressdialog():
    widgets.ProgressDialog()


def test_pushbutton():
    widget = widgets.PushButton("Test")
    widget.set_disabled()
    widget.set_enabled()
    widget.set_icon("mdi.timer")
    widget.set_style_icon("close")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


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


def test_statusbar():
    widget = widgets.MainWindow()
    status_bar = widgets.StatusBar()
    status_bar.set_color("black")
    label = widgets.Label("test")
    status_bar.addWidget(label)
    status_bar.setup_default_bar()
    widget.setStatusBar(status_bar)


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
    return True


def test_spinbox():
    widget = widgets.SpinBox()
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
    widget.set_expanding()
    widget.set_orientation("horizontal")


def test_tabwidget():
    widget = widgets.TabWidget()
    widget.add_tab(widgets.Widget(), "mdi.timer")
    widget.insert_tab(0, widgets.Widget(), "test", "mdi.timer")
    w = widgets.Widget()
    widget.add_tab(w, "test", "mdi.timer")
    assert widget[2] == w
    widget.set_tab(0, "right", None)
    widget.set_detachable()
    widget.detach_tab(0, core.Point())
    widget.remove_tab(0)
    # widget.close_detached_tabs()


def test_textbrowser():
    widget = widgets.TextBrowser()
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


def test_textedit():
    widget = widgets.TextEdit()
    widget.set_text("test")
    widget.append_text(" this")
    assert widget.text() == "test\n this"
    widget.set_font("Consolas")
    widget.set_enabled()
    widget.set_read_only()
    widget.scroll_to_bottom()
    widget.set_disabled()
    widget.set_color("black")
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)


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
    widget.set_font_size(10)
    widget.set_enabled()
    widget.set_disabled()

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


def test_tabbar():
    widget = widgets.TabBar()
    widget.set_icon_size(20)


def test_tableview():
    widget = widgets.TableView()
    widget.set_selection_mode("extended")
    widget.set_selection_behaviour("rows")
    widget.set_horizontal_scrollbar_visibility("always_on")
    widget.set_vertical_scrollbar_visibility("always_on")
    widget.set_horizontal_scrollbar_width(12)
    widget.set_vertical_scrollbar_width(12)
    widget.set_edit_triggers("edit_key")
    widget.selectAll()
    widget.current_index()
    widget.current_data()
    widget.adapt_sizes()
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.num_selected()
    widget.jump_to_column(0)
    widget.highlight_when_inactive()


def test_toolbox():
    w = widgets.RadioButton("test1")
    w2 = widgets.RadioButton("test2")
    w2.setObjectName("test_name")
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
    model = widgets.FileSystemModel()
    widget.setModel(model)
    widget.selectAll()
    widget.h_header()
    widget.setup_list_style()
    widget.setup_dragdrop_move()
    widget.current_index()
    widget.set_selection_mode("extended")
    widget.set_selection_behaviour("rows")
    widget.set_horizontal_scrollbar_visibility("always_on")
    widget.set_vertical_scrollbar_visibility("always_on")
    widget.set_horizontal_scrollbar_width(12)
    widget.set_vertical_scrollbar_width(12)
    widget.num_selected()
    widget.jump_to_column(0)
    widget.highlight_when_inactive()
    widget.raise_dock()
    widget.adapt_sizes()


def test_widget():
    widget = widgets.Widget()
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


def test_widgetaction():
    action = widgets.Action()
    widgetaction = widgets.WidgetAction(action)
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
