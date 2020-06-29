#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import re

from qtpy import QtCore, QtGui

import prettyqt.custom_widgets.dataset as fo
from prettyqt import core, custom_widgets, gui, widgets

test_widget = widgets.Widget()


def test_booldicttoolbutton():
    dct = dict(a="test",
               b="test2")
    w = custom_widgets.BoolDictToolButton("Title", None, dct)
    w["a"] = True
    assert w["a"] is True
    assert w.as_dict() == dict(a=True, b=False)


def test_buttondelegate():
    widget = custom_widgets.ButtonDelegate(parent=None)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    widget.currentIndexChanged()


def test_radiodelegate():
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(['LIB', 'CELL', 'area'])
    item = widgets.TableWidgetItem("test")
    widget.setItem(0, 0, item)
    widget.setItem(1, 1, widgets.TableWidgetItem("test"))
    delegate = custom_widgets.RadioDelegate(widget, ["a", "b"])
    widget.setItemDelegateForColumn(0, delegate)
    widget.openPersistentEditor(item)


def test_colorchooserbutton():
    btn = custom_widgets.ColorChooserButton()
    btn.set_color("green")
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    repr(btn)
    assert btn.get_value() == gui.Color("green")
    btn.set_value("blue")
    assert btn.is_valid()


def test_regexeditor():
    widget = custom_widgets.RegexEditorWidget()
    widget.regex = "[0-9]"
    assert widget.regex == "[0-9]"
    widget.string = "test123"
    assert widget.string == "test123"
    widget.compile_flags = re.IGNORECASE


def test_dataset():

    class Test(fo.DataSet):
        i1 = fo.Bool(label="My first one")
        string1 = fo.String(label="My first one", regex="[0-9]")
        string2 = fo.String(label="My second one", notempty=True)
        choiceitem = fo.Enum(label="A", choices=["A", "B"]).set_not_active("i1")
        mchoiceitem = fo.MultipleChoice(label="A", choices=["A", "B"])
        floatitem = fo.Float(label="FloatItem").set_active("i1")
        intitem = fo.Int(label="IntItem").set_active("i1")
        coloritem = fo.Color(label="ColorItem", value="green")
        fileitem = fo.File(label="File")
        folderitem = fo.Folder(label="File", optional="Test")
        stringornumber = fo.StringOrNumber(label="Test")
        buttonitem = fo.Button(label="Button", callback=print)
        intlist = fo.IntList(label="Button", value=[1, 2, 3])
        intlist = fo.FloatList(label="Button", value=[1.1, 2, 3])
        code = fo.Code(label="Test", value="class Test")

    settings = Test(icon="mdi.timer")
    settings.create_dialog()
    settings.to_dict()


def test_stringornumberwidget():
    widget = custom_widgets.StringOrNumberWidget()
    widget.get_value()
    widget.on_value_change()


def test_optionalwidget():
    w = widgets.RadioButton()
    container = custom_widgets.OptionalWidget(w, "Test")
    container.get_value()
    container.enabled = False
    assert container.enabled is False


def test_singlelinetextedit():
    w = custom_widgets.SingleLineTextEdit()
    w.set_text("test")


def test_mappedcheckbox():
    widget = custom_widgets.MappedCheckBox(true_value=0, false_value=1)
    widget.set_value(0)
    assert widget.get_value() == 0
    widget.setChecked(False)
    assert widget.get_value() == 1


def test_filechooserbutton():
    btn = custom_widgets.FileChooserButton()
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.set_value("/")
    btn.get_value()


def test_fontchooserbutton():
    btn = custom_widgets.FontChooserButton()
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.set_font("Consolas")
    repr(btn)


def test_iconlabel():
    w = custom_widgets.IconLabel()
    w.set_text("test")
    assert w.text() == "test"
    repr(w)


def test_inputandslider():
    w = custom_widgets.InputAndSlider()
    w.set_range(0, 10)
    w.set_value(5)
    assert w.get_value() == 5
    w.set_step_size(2)
    assert w.is_valid()


def test_codeeditor():
    editor = custom_widgets.CodeEditor()
    assert editor.text() == ""
    editor.line_area_width()
    editor.set_syntax("python")
    event = QtGui.QResizeEvent(core.Size(10, 10), core.Size(20, 20))
    editor.resizeEvent(event)
    event = QtGui.QPaintEvent(core.Rect(0, 0, 20, 20))
    editor.line_area_paintevent(event)


def test_imageviewer():
    custom_widgets.ImageViewer()


def test_flowlayout():
    widget = widgets.Widget()
    layout = custom_widgets.FlowLayout(margin=1)
    btn = widgets.PushButton("Short")
    layout += btn
    layout += widgets.PushButton("Longer")
    layout += widgets.PushButton("Different text")
    layout += widgets.PushButton("More text")
    layout += widgets.PushButton("Even longer button text")
    layout.do_layout(core.Rect(), False)
    layout.sizeHint()
    widget.set_layout(layout)
    assert layout[0] == btn
    for i in layout:
        pass
    assert len(layout) == 5
    layout.get_children()
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)


def test_labeledslider(qtbot):
    slider = custom_widgets.LabeledSlider(["test1", "test2"], "vertical")
    slider = custom_widgets.LabeledSlider(["test1", "test2"])
    qtbot.addWidget(slider)
    qtbot.mouseClick(slider.sl, QtCore.Qt.LeftButton)
    qtbot.mouseMove(slider.sl, core.Point(20, 20))
    slider.paintEvent(None)


def test_markdownwidget():
    custom_widgets.MarkdownWindow()


def test_popupinfo():
    popup = custom_widgets.PopupInfo()
    popup.show_popup("test")


def test_promptlineedit():
    widget = custom_widgets.PromptLineEdit()
    widget.prompt_text = "test"
    assert widget.prompt_text == "test"
    widget.set_button_visible(True)
    widget.set_button_visible(False)
    widget.set_text("test")


def test_selectionwidget():
    widget = custom_widgets.SelectionWidget()

    class Test(object):
        pass
    test = Test()
    items = {"Semicolon": ";",
             "Tab": "tab",
             "Comma": ",",
             "class": test}
    widget.add_items(items)
    widget.add_items(("a", "b"))
    widget.add_tooltip_icon("test")
    widget.add_custom(label="test", regex=r"\S{1}")
    radiobuttons = [k for k, v in widget.buttons.items()]
    radiobuttons[1].click()
    assert widget.get_value() == "tab"
    radiobuttons[3].click()
    assert widget.current_choice() == test
    for i in widget:
        pass
    widget.select_radio_by_data(";")
    choice = widget.current_choice()
    assert choice == ";"
    widget.set_value(",")
    assert widget.get_value() == ","
    widget.update_choice(True)


def test_spanslider(qtbot):
    slider = custom_widgets.SpanSlider()
    qtbot.addWidget(slider)
    slider.set_lower_value(10)
    slider.set_upper_value(20)
    slider.set_lower_pos(15)
    slider.set_upper_pos(25)
    assert slider.lower_value == 15
    assert slider.upper_value == 25
    slider.set_lower_value(12)
    slider.set_upper_pos(20)
    color = gui.Color("blue")
    slider.set_left_color(color)
    slider.set_right_color(color)
    slider.swap_controls()
    slider.trigger_action(slider.SliderNoAction, True)
    slider.trigger_action(slider.SliderSingleStepAdd, True)
    slider.paintEvent(None)
    slider.pixel_pos_to_value(100)
    slider.draw_span(gui.Painter(), core.Rect())
    slider.move_pressed_handle()
    qtbot.mouseClick(slider, QtCore.Qt.LeftButton)
    qtbot.mouseMove(slider, core.Point(20, 20))
    qtbot.mouseMove(slider, core.Point(0, 0), delay=10)
    assert slider.movement_mode == "free"
    slider.set_movement_mode("no_overlap")


def test_waitingspinner():
    spinner = custom_widgets.WaitingSpinner(parent=test_widget)
    spinner.paintEvent(None)
    spinner.set_line_num(2)
    assert spinner.line_num() == 2
    spinner.set_line_length(2)
    assert spinner.line_length() == 2
    spinner.set_line_width(2)
    assert spinner.line_width() == 2
    spinner.set_inner_radius(2)
    assert spinner.inner_radius() == 2
    spinner.set_color("black")
    spinner.set_revolutions_per_second(2)
    spinner.set_trail_fade_percentage(2)
    spinner.set_minimum_trail_opacity(2)
    spinner.rotate()
    spinner.start()
    spinner.stop()
    spinner.update_position()
